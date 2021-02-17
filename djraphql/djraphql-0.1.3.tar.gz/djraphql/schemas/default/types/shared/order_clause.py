from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from graphene import InputObjectType, Enum
from djraphql.util.django_models import get_concrete_fields


class SortDirection(Enum):
    asc = "ascending"
    desc = "descending"


class OrderClause(CacheableTypeBuilder, AbstractTypeBuilder):
    @staticmethod
    def make(registry, **kwargs):
        # Build where predicate InputObjects to allow filtering in queries.
        order_by_type_attrs = {}
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)
        for field in get_concrete_fields(model_class, registry.available_model_classes):
            if entity_class._field_is_excluded_or_not_included(field):
                continue

            # Convert names of ForeignKey/OneToOneFields from 'foo' to 'foo_id'
            field_name = field.name
            if field.many_to_one or field.one_to_one and field_name != "id":
                field_name = "{}_id".format(field_name)
            order_by_type_attrs[field_name] = SortDirection()

        return type(
            "OrderBy{}".format(model_class.__name__),
            (InputObjectType,),
            order_by_type_attrs,
        )
