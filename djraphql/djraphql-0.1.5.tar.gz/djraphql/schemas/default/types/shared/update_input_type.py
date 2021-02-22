from djraphql.util.django_models import get_target_field
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
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)
        for model_field in registry.get_model_fields(model_class).values():
            field = model_field.get_django_model_field(model_class)

            # Don't allow updating the field is it is (part of) a PK,
            # or it's not included in the Entity.Meta.fields list,
            # or it is read-only.
            if (field.concrete and field.primary_key) or model_field.read_only:
                continue

            if (
                field.is_relation
                and not registry.get_entity_class(field.related_model).is_updatable()
            ):
                # We don't allow the related object to be updated, but we do allow
                # the reference to it to change, i.e., if a Foo has a FK to a Bar,
                # we allow foo.bar_id to be updated (given that a Foo is updatable).
                if field.concrete:
                    # If the related model's entity overrides get_for_insert,
                    # that implies that this field is read-only.
                    related_entity = registry.get_entity_class(field.related_model)
                    if related_entity.can_get_for_insert():
                        continue

                    reverse_model_field = registry.get_model_fields(
                        field.related_model
                    )[get_target_field(field).name]

                    graphene_type = reverse_model_field.get_graphene_type(
                        field.related_model, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                    )
                    input_class_attrs["{}_id".format(field.name)] = graphene_type()
                continue

            if field.one_to_many:
                list_update_input_type = registry.get_or_create_type(
                    Types.LIST_UPDATE_INPUT_TYPE, model_class=field.related_model
                )
                input_class_attrs[field.name] = Field(list_update_input_type)
            elif field.many_to_one or field.one_to_one:
                if field.concrete:
                    reverse_model_field = registry.get_model_fields(
                        field.related_model
                    )[get_target_field(field).name]

                    graphene_type = reverse_model_field.get_graphene_type(
                        field.related_model, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                    )
                    input_class_attrs["{}_id".format(field.name)] = graphene_type()
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
                input_class_attrs[field.name] = model_field.get_graphene_type(
                    model_class, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                )()

        return type(
            "{}UpdateInput".format(model_class.__name__),
            (InputObjectType,),
            input_class_attrs,
        )
