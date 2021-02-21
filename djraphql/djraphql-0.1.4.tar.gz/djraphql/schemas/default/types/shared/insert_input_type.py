from djraphql.util.django_models import get_target_field
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
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)

        for model_field in registry.get_model_fields(model_class).values():
            field = model_field.get_django_model_field(model_class)

            if (field.concrete and field.primary_key) or model_field.read_only:
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
                related_entity = registry.get_entity_class(field.related_model)
                if related_entity.can_get_for_insert():
                    continue

                # If the field is concrete, define a *_id field so that, e.g., we
                # can insert an Album with a labelId.
                if field.concrete:
                    reverse_model_field = registry.get_model_fields(
                        field.related_model
                    )[get_target_field(field).name]

                    graphene_type = reverse_model_field.get_graphene_type(
                        field.related_model, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                    )
                    input_class_attrs["{}_id".format(field.name)] = graphene_type()

                # Check that the related object type is creatable and if it is, allow
                # a nested create by defining the related model's insert input type.
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
                input_class_attrs[field.name] = model_field.get_graphene_type(
                    model_class, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                )(required=not field.null and not field.has_default())

        return type(
            "{}Input".format(model_class.__name__),
            (InputObjectType,),
            input_class_attrs,
        )
