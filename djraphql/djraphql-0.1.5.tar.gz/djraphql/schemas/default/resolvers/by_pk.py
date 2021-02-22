from ..util.query_optimization import get_prefetched_queryset


def build_by_pk_resolver(model_class, registry):
    entity_class = registry.get_entity_class(model_class)

    def by_pk_resolver(parent, info, **kwargs):

        if not entity_class.is_readable_by_context(info.context):
            raise Exception("Invalid permissions.")

        queryset = entity_class.get_queryset(info.context).filter(**kwargs)

        result = get_prefetched_queryset(queryset, registry, info)

        return result.get()

    return by_pk_resolver
