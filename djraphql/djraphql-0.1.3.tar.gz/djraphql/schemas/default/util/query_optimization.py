from graphql.language.visitor import visit
from django.db.models.query import Prefetch
from .visitors import QuerySelectionVisitor
from .arguments import update_queryset_based_on_arguments


def get_prefetched_queryset(queryset, registry, info):
    # Problem: We allow a caller to specify e.g. a 'where' filter in a
    # GraphQL query at any level of the query: root, child, grandchild, ...
    # When there is a 'where' at a non-root level, we will fall victim
    # to the N+1 problem and issue as many queries as there are children.
    # Solution: To avoid N+1 queries, we traverse the GraphQL query's AST
    # to find opportunities to use Django's Prefetch objects.
    # Example: consider the following query
    # query {
    #   albums(where: {author: _eq: "bob"}}) {
    #     name
    #     releaseDate
    #     songs(where: {starCount: {_eq: 5}}) {
    #       id
    #       name
    #       starredBy {
    #         name
    #       }
    #     }
    #   }
    # }
    # If bob has released 5 albums, and on each of those albums, 3 songs
    # have 5 stars, then:
    # 1x query for albums where bob is the author... returns 5 albums
    # 5x (5 albums) query for 5-star songs on each album... each query returns 3 songs
    # 15x (3 songs x 5 albums) query for the names of the people that
    # starred the song.
    # For a grand total of 75 queries to the database in a single request!
    # Using Prefetch can bring that down the number of level deep
    # the query goes, which in this case is 3.

    # Use the SelectedFieldsVisitor to execute
    # (a) Updating the queryset to only fetch the columns necessary to fulfill the request
    # (b) Updating the queryset to prefetch/select relate fields to avoid N+1
    visitor = SelectedFieldsVisitor(queryset, registry, info)
    visit(info.field_asts[0], visitor)
    return visitor.queryset


class NodeInfo(object):
    def __init__(self, key, model_class, field_names, arguments=None):
        self.key = key
        self.model_class = model_class
        self.field_names = field_names
        self.select_related_keys = []
        self.arguments = arguments


class SelectedFieldsVisitor(QuerySelectionVisitor):
    def __init__(self, queryset, type_registry, info):
        self.queryset = queryset
        self.prefetch_stack = []
        self.prefetch_info_by_key = {}
        super(SelectedFieldsVisitor, self).__init__(type_registry, info)

    def enter_field(self, field, arguments):

        if field.is_relation:
            # Subtle thing here to account for how ORM optimizes query prefetching.
            # If the field is concrete, we need to add the field's name to the
            # field names for the node we're leaving.
            # If not concrete we need to add the reverse related name to the
            # field names for the node we're entering.
            field_names = []
            if field.concrete:
                self.prefetch_stack[-1].field_names.append(field.name)
            else:
                field_names = [field.field.name]

            # Push a NodeInfo onto the stack.
            self.prefetch_stack.append(
                NodeInfo(field.name, field.related_model, field_names, arguments)
            )

        else:
            # This is just a scalar, which we add to the top of the stack's
            # list of field names to be passed to .only() later.
            self.prefetch_stack[-1].field_names.append(field.name)

    def leave_field(self, field):

        # If we aren't leaving a relational field, there's nothing to do
        if not field.is_relation:
            return

        if field.one_to_many or field.many_to_many:
            # *-to-many relations are handled via a later prefetch_related,
            # so we need to perform some bookkeeping by updating prefetch_info_by_key.
            key_path = "__".join([pi.key for pi in self.prefetch_stack if pi.key])
            prefetch_info = self.prefetch_stack.pop()
            self.prefetch_info_by_key[key_path] = prefetch_info
        elif field.one_to_one or field.many_to_one:
            # *-to-one relations are handled via a later select_related,
            # we've got bookkeeping here as well, but it's a bit more complex.
            # We must collapse/coalesce the top 2 items in the prefetch_stack.
            to_one = self.prefetch_stack.pop()

            # Add the popped item's key to the new top item's select_related_keys list.
            self.prefetch_stack[-1].select_related_keys.append(to_one.key)

            # Add the popped item's select_related_keys to the new top item's
            # select_related_keys, each prefixed with the popped item's key.
            for select_related_key in to_one.select_related_keys:
                self.prefetch_stack[-1].select_related_keys.append(
                    "{}__{}".format(to_one.key, select_related_key)
                )

            # Add the popped item's field_names to the new top item's field_names,
            # but prefixed with the popped item's key.
            for field_name in to_one.field_names:
                self.prefetch_stack[-1].field_names.append(
                    "{}__{}".format(to_one.key, field_name)
                )

    def enter_optimizable_tree(self, model_class, arguments):
        self.prefetch_stack.append(NodeInfo(None, model_class, [], arguments))

    def leave_optimizable_tree(self, model_class):
        # Construct the Prefetches from the information we gathered
        # as we traversed the query selections tree.
        # Why do we sort the keys? Because we ran into an issue where
        # if we process e.g. ['artists__albums', 'artists'], Django complains:
        # ValueError("'artists' lookup was already seen with a different queryset.
        # You may need to adjust the ordering of your lookups.",)
        # Oddly, the error does not happen when processed in order
        # like ['artists', 'artists__albums']. So we sort the keys. This will
        # probably blow up in unexpected ways but theoretically the order shouldn't
        # matter at all, so if ordering them to appease Django works, it feels OK.
        to_many_sorted_keys = sorted(self.prefetch_info_by_key.keys())
        for key in to_many_sorted_keys:
            prefetch_info = self.prefetch_info_by_key[key]

            # Only select the columns necessary to fulfill the request
            prefetch_queryset = prefetch_info.model_class.objects.only(
                *prefetch_info.field_names
            )

            # Prefetches (which generally map to *-to-many relations of the root
            # object) can have nested *-to-one relations which we need to fetch
            # via select_related. This minimizes the # of queries Django ORM executes.
            if prefetch_info.select_related_keys:
                prefetch_queryset = prefetch_queryset.select_related(
                    *prefetch_info.select_related_keys
                )

            # Call prefetch_related, passing in the Prefetch object that contains
            # our optimizations plus filtering for any arguments from the query.
            self.queryset = self.queryset.prefetch_related(
                Prefetch(
                    key,
                    queryset=update_queryset_based_on_arguments(
                        prefetch_queryset,
                        prefetch_info.arguments,
                        take_slice=False,
                    ),
                )
            )

        # The prefetch_stack should now have a single item, which maps
        # to the root object in the query. Select only necessary columns and filter
        # via any arguments passed in.
        root_info = self.prefetch_stack.pop()
        self.queryset = update_queryset_based_on_arguments(
            self.queryset.only(*root_info.field_names),
            root_info.arguments,
        )

        # Finally, add any necessary select_related calls.
        if root_info.select_related_keys:
            self.queryset = self.queryset.select_related(*root_info.select_related_keys)
