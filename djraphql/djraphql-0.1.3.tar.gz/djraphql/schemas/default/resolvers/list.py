from ..util.query_optimization import get_prefetched_queryset
from ..util.arguments import (
    DEFAULT_MAXIMUM_RESULTS,
    ABSOLUTE_MAXIMUM_RESULTS,
    update_queryset_based_on_arguments,
)


def build_list_resolver(model_class, registry, related_name=None):
    entity_class = registry.get_entity_class(model_class)

    def list_resolver(parent, info, **kwargs):

        if not entity_class.is_readable_by_context(info.context):
            raise Exception("Invalid permissions.")

        # If related_name and parent are not None, then we are resolving a
        # subselect, which has already been prefetched via the code below.
        if related_name and parent is not None:
            # If we have limit/offset arguments, we did *not* prefetch earlier,
            # so we must query by filtering the parent's .all() method.
            # This is related to the limit/offset issue described below.
            queryset = getattr(parent, related_name).get_queryset()
            if kwargs.get("limit") or kwargs.get("offset"):
                if queryset.count() < 10000:
                    # Load all rows (if less than 1000) into memory before slicing
                    limit = kwargs.get("limit") or DEFAULT_MAXIMUM_RESULTS
                    if limit > ABSOLUTE_MAXIMUM_RESULTS:
                        limit = ABSOLUTE_MAXIMUM_RESULTS
                    offset = kwargs.get("offset") or 0
                    return list(queryset)[offset : offset + limit]
                else:
                    # Too much to load into memory at once... so N+1 :(
                    return update_queryset_based_on_arguments(
                        getattr(parent, related_name).all(), kwargs
                    )

            return queryset

        # We're resolving a top-level select, so we must filter by org,
        # which is done by running the check lambda provided by the caller
        queryset = entity_class.get_queryset(info.context)
        return get_prefetched_queryset(queryset, registry, info)

    return list_resolver
