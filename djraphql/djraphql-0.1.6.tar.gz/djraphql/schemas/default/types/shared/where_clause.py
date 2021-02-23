from ....abstract_type_builder import AbstractTypeBuilder, CacheableTypeBuilder
from graphene import List, InputObjectType, Boolean, Field
from ...mappings import Types, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES


class WhereClause(CacheableTypeBuilder, AbstractTypeBuilder):
    @staticmethod
    def make(registry, **kwargs):
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)

        # Build where predicate InputObjects to allow filtering in queries.
        where_input_type_attrs = {}
        for model_field in registry.get_model_fields(model_class).values():
            field = model_field.get_django_model_field(model_class)

            if field.is_relation:
                if field.many_to_one or field.one_to_many:
                    where_input_type_attrs[field.name] = Field(
                        registry.lambda_from_registry(
                            field.related_model, Types.WHERE_CLAUSE_TYPE
                        )
                    )

            if not field.concrete:
                continue

            # TODO: Remove when support for many to many is implemented
            if field.many_to_many:
                continue

            # Convert names of ForeignKey/OneToOneFields from 'foo' to 'foo_id'
            field_name = field.name
            if field.many_to_one or field.one_to_one and field_name != "id":
                field_name = "{}_id".format(field_name)

            # The predicate input types for e.g. IntegerFields need different type
            # definitions than CharFields.
            # e.g., where: {id: _eq: 1} vs. where: {name: _eq: "hello"}
            # Examine the type of a model's field and build the appropriately typed
            # predicate input objects.
            type_name = field.get_internal_type()
            if field.choices:
                enum_type = registry.get_or_create_type(
                    Types.ENUM_TYPE,
                    model_class=model_class,
                    field=field,
                    choices=field.choices,
                )
                where_input_type_attrs[field_name] = type(
                    "WherePredicate{}".format(enum_type.__name__),
                    (InputObjectType,),
                    {
                        "_eq": enum_type(name="_eq"),
                        "_neq": enum_type(name="_neq"),
                        "_in": List(enum_type, name="_in"),
                        "_nin": List(enum_type, name="_nin"),
                        "_is_null": Boolean(name="_is_null"),
                    },
                )()
            else:
                graphene_type = model_field.get_graphene_type(
                    model_class, DJANGO_TYPE_NAMES_TO_GRAPHENE_TYPES
                )
                where_input_type_attrs[field_name] = registry.get_or_create_type(
                    Types.WHERE_PREDICATE_INPUT_TYPE,
                    graphene_type=graphene_type,
                )()

        # These fields are always the same, they just recursively reference the
        # input type we're building.
        where_input_lambda = registry.lambda_from_registry(
            model_class, Types.WHERE_CLAUSE_TYPE
        )
        where_input_type_attrs["_and"] = List(where_input_lambda, name="_and")
        where_input_type_attrs["_or"] = List(where_input_lambda, name="_or")
        where_input_type_attrs["_not"] = Field(where_input_lambda, name="_not")

        return type(
            "Where{}".format(model_class.__name__),
            (InputObjectType,),
            where_input_type_attrs,
        )
