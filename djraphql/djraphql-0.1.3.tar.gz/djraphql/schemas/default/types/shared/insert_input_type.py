from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from ...mappings import DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES, Types
from graphene import Field, InputObjectType, List


class InsertInputType(CacheableTypeBuilder, AbstractTypeBuilder):
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

            if entity_class._field_is_excluded_or_not_included(field):
                continue

            if entity_class._field_is_read_only(field):
                continue

            if field.one_to_many:
                related_entity = registry.get_entity_class(field.related_model)
                if related_entity.is_creatable():
                    input_class_attrs[field.name] = List(
                        registry.get_or_create_type(
                            Types.NESTED_ITEM_INSERT_TYPE,
                            model_class=field.related_model,
                        )
                    )
            elif field.many_to_one or field.one_to_one:
                # If the field is concrete, define a *_id field so that, e.g., we
                # can insert an Album with a labelId.
                if field.concrete:
                    input_class_attrs[
                        "{}_id".format(field.name)
                    ] = DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[field.get_internal_type()]()

                # Check that the related object type is creatable and if it is, allow
                # a nested create by defining the related model's insert input type.
                related_entity = registry.get_entity_class(field.related_model)
                if field.is_relation and related_entity.is_creatable():
                    input_class_attrs[field.name] = Field(
                        registry.lambda_from_registry(
                            field.related_model, Types.INSERT_INPUT_TYPE
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
                input_class_attrs[field.name] = Field(
                    enum_type, required=not field.null and field.default is None
                )
            else:
                input_class_attrs[field.name] = DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[
                    field.get_internal_type()
                ](required=not field.null and not field.has_default())

        return type(
            "{}Input".format(model_class.__name__),
            (InputObjectType,),
            input_class_attrs,
        )
