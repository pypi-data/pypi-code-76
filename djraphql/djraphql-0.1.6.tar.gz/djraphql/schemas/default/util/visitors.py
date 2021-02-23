from six import iteritems
from graphql.language.visitor import Visitor
from graphene.utils.str_converters import to_snake_case
from djraphql.util.django_models import get_field_by_name
from graphql.execution.base import get_field_def
from graphql.execution.values import get_argument_values


class QuerySelectionVisitor(Visitor):
    def __init__(self, type_registry, info):
        self.type_lookup = type_registry._node_graphql_type_name_to_model_class
        self.info = info
        self.graphql_type_stack = [info.parent_type]
        self.model_class_stack = []

    def _get_terminal_gql_type(self, gql_type):
        while hasattr(gql_type, "of_type"):
            gql_type = gql_type.of_type
        return gql_type

    def enter_Field(
        self,
        node,
        key,
        parent,
        path,
        ancestors,
    ):
        # Get the parent type of this field
        parent_gql_type = self.graphql_type_stack[-1]

        # Get a dictionary of the arguments associated with this field
        field_def = get_field_def(self.info.schema, parent_gql_type, node.name.value)
        arguments = get_argument_values(
            field_def.args,
            node.arguments,
            self.info.variable_values,
        )

        # Do we call enter_field?
        if parent_gql_type.name in self.type_lookup:
            model_class = self.type_lookup[parent_gql_type.name]["model_class"]
            field = try_get_related_field(model_class, node.name.value)
            if field:
                self.enter_field(field, arguments)

        # If we're traversing a relationship (e.g., we're entering the
        # "artists" node within the "LabelsMany" query), we need to push the new
        # GraphQLTypeObject class and model class onto their respective stacks.
        if node.selection_set:
            maybe_nonterminal_gql_type = parent_gql_type.fields.get(
                node.name.value
            ).type
            next_gql_type = self._get_terminal_gql_type(maybe_nonterminal_gql_type)
            self.graphql_type_stack.append(next_gql_type)

            if next_gql_type.name in self.type_lookup:
                model_class = self.type_lookup[next_gql_type.name]["model_class"]
                if not self.model_class_stack:
                    self.enter_optimizable_tree(model_class, arguments)
                self.model_class_stack.append(model_class)

    def enter_optimizable_tree(self, model_class):
        pass

    def leave_optimizable_tree(self, model_class):
        pass

    def enter_field(self, field):
        pass

    def leave_field(self, field):
        pass

    def leave_Field(
        self,
        node,
        key,
        parent,
        path,
        ancestors,
    ):
        # If we're traversing a relationship, e.g. we're leaving the "artists" node
        # within the "LabelsMany" query, we need to pop our GraphQLType stack
        # and _possibly_ our model stack.
        if node.selection_set:
            self.graphql_type_stack.pop()
            if len(self.model_class_stack) == 1:
                # We're about to pop the last item from our model stack,
                # that means we're exiting the optimizable tree, so call that handler.
                self.leave_optimizable_tree(self.model_class_stack.pop())
            elif self.model_class_stack:
                # There will still be items left in our model stack, we're still
                # within the optimizable tree. In this case, call leave_field.
                self.model_class_stack.pop()
                field = try_get_related_field(
                    self.model_class_stack[-1], node.name.value
                )
                if field:
                    self.leave_field(field)
            return

        # We are not traversing a relationship. If we have a non-empty
        # model stack, we need to call the leave_field handler.
        if self.model_class_stack:
            field = try_get_related_field(self.model_class_stack[-1], node.name.value)
            if field:
                self.leave_field(field)


def try_get_related_field(model_class, selection_name):
    names_to_try = [
        # First try just getting the field from the model via the selection's name
        # in the GraphQL query. This is usually a camelCased name. We do this in
        # case the user has defined their model's related_name(s)
        # in camelCase instead of snake_case
        selection_name,
        # Next, attempt to get the field by snake_casing the name of the selection.
        to_snake_case(selection_name),
    ]

    for name in names_to_try:
        try:
            return get_field_by_name(model_class, name)
        except:  # FieldDoesNotExist
            pass
