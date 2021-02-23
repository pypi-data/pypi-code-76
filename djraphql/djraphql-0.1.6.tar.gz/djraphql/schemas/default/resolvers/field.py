def build_field_resolver(field):
    def resolve_field(parent, info, **kwargs):
        return getattr(parent, field.name, None)

    return resolve_field
