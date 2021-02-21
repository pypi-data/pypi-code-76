from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from ...mappings import DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
from graphene import Field, InputObjectType
from djraphql.util.django_models import get_pk_fields_for_model


class PkInputType(CacheableTypeBuilder, AbstractTypeBuilder):
    @staticmethod
    def make(registry, **kwargs):
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)
        pk_fields = registry.get_pk_fields_for_model(model_class)

        if len(pk_fields) == 1:
            model_field = registry.get_model_fields(model_class)[pk_fields[0].name]
            return model_field.get_graphene_type(
                pk_fields[0].model, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
            )

        return type(
            "{}PKInputType".format(model_class.__name__),
            (InputObjectType,),
            {
                field.name: Field(
                    DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES[field.get_internal_type()],
                    required=True,
                )
                for field in pk_fields
            },
        )
