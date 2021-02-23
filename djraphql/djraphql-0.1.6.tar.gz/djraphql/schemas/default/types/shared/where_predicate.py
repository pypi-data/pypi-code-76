from ....abstract_type_builder import AbstractTypeBuilder
from graphene import Boolean, InputObjectType, List
from ...mappings import DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES


class WherePredicate(AbstractTypeBuilder):
    @classmethod
    def cache_key(cls, type_key, **kwargs):
        graphene_type = kwargs["graphene_type"]
        return graphene_type.__name__

    @staticmethod
    def make(registry, **kwargs):
        graphene_type = kwargs["graphene_type"]
        return type(
            "WherePredicate{}".format(graphene_type.__name__),
            (InputObjectType,),
            {
                "_eq": graphene_type(name="_eq"),
                "_neq": graphene_type(name="_neq"),
                "_gt": graphene_type(name="_gt"),
                "_gte": graphene_type(name="_gte"),
                "_lt": graphene_type(name="_lt"),
                "_lte": graphene_type(name="_lte"),
                "_in": List(graphene_type, name="_in"),
                "_nin": List(graphene_type, name="_nin"),
                "_is_null": Boolean(name="_is_null"),
                "_like": graphene_type(name="_like"),
                "_ilike": graphene_type(name="_ilike"),
            },
        )
