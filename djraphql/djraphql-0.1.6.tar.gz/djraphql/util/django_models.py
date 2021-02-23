def get_pk_fields_for_model(model_class, available_model_classes):
    return tuple(
        [
            f
            for f in model_class._meta.get_fields()
            if getattr(f, "primary_key", False)
            and (not f.is_relation or f.related_model in available_model_classes)
        ]
    )


def get_field_by_name(model_class, field_name):
    # Django 1.11.17+
    if hasattr(model_class._meta, "get_field"):
        return model_class._meta.get_field(field_name)

    # Django 1.8+
    if hasattr(model_class._meta, get_field_by_name):
        return model_class._meta.get_field_by_name(field_name)[0]

    raise Exception("Cannot fetch {} field {}.".format(model_class, field_name))


def get_target_field(relational_field):
    # Django 2+
    if hasattr(relational_field, "target_field"):
        return relational_field.target_field

    # Django 1.8+
    if hasattr(relational_field, "related_field"):
        return relational_field.related_field

    raise Exception("Cannot get target field on field {}.".format(relational_field))
