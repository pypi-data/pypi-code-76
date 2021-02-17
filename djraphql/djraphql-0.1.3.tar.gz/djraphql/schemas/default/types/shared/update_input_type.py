from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from ...mappings import DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES, Types
from graphene import Field, InputObjectType


class UpdateInputType(CacheableTypeBuilder, AbstractTypeBuilder):
    @staticmethod
    def make(registry, **kwargs):
        """Generates a Graphene InputObjectType for the associated model.
        https://docs.graphene-python.org/en/latest/types/mutations/#inputfields-and-inputobjecttypes
        """
        input_class_attrs = {}
        available_model_classes = registry.available_model_classes
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)
        for field in model_class._meta.get_fields():
            if field.concrete and field.primary_key:
                continue

            if field.is_relation and field.related_model not in available_model_classes:
                continue

            if (
                field.is_relation
                and not registry.get_entity_class(field.related_model).is_updatable()
            ):
                # We don't allow the related object to be updated, but we do allow
                # the reference to it to change, i.e., if a Foo has a FK to a Bar,
                # we allow foo.bar_id to be updated (given that a Foo is updatable).
                if field.concrete:
                    input_class_attrs[
                        "{}_id".format(field.name)
                    ] = DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[field.get_internal_type()]()
                continue

            if entity_class._field_is_excluded_or_not_included(field):
                continue

            if entity_class._field_is_read_only(field):
                continue

            if field.one_to_many:
                list_update_input_type = registry.get_or_create_type(
                    Types.LIST_UPDATE_INPUT_TYPE, model_class=field.related_model
                )
                input_class_attrs[field.name] = Field(list_update_input_type)
            elif field.many_to_one or field.one_to_one:
                if field.concrete:
                    input_class_attrs[
                        "{}_id".format(field.name)
                    ] = DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[field.get_internal_type()]()
                related_model = field.related_model
                input_class_attrs[field.name] = Field(
                    registry.lambda_from_registry(
                        related_model, Types.UPDATE_INPUT_TYPE
                    )
                )
            elif field.many_to_many:
                pass
            elif field.choices:
                enum_type = registry.get_or_create_type(
                    Types.ENUM_TYPE,
                    model_class=model_class,
                    field=field,
                    choices=field.choices,
                )
                input_class_attrs[field.name] = Field(enum_type, required=False)
            else:
                input_class_attrs[field.name] = DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[
                    field.get_internal_type()
                ]()

        return type(
            "{}UpdateInput".format(model_class.__name__),
            (InputObjectType,),
            input_class_attrs,
        )
