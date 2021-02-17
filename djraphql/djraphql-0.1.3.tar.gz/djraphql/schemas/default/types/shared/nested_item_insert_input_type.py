from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from ...mappings import Types
from graphene import Field, InputObjectType, String


class NestedItemInsertInputType(CacheableTypeBuilder, AbstractTypeBuilder):
    @staticmethod
    def make(registry, **kwargs):
        input_class_attrs = {}
        model_class = kwargs["model_class"]

        return type(
            "NestedItemInsert{}".format(model_class.__name__),
            (InputObjectType,),
            {
                "tag": Field(String),
                "data": Field(
                    registry.lambda_from_registry(model_class, Types.INSERT_INPUT_TYPE),
                    required=True,
                ),
            },
        )
