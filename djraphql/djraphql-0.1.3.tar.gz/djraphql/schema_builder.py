from graphene import ObjectType
from .type_registry import TypeRegistry
from .schemas.default import DefaultSchema


class SchemaBuilder(object):
    def __init__(self, schema=None):
        self.schema = schema or DefaultSchema()
        self.registry = TypeRegistry(self.schema)

    def register_entity_classes(self, *entity_classes):
        self.registry.register_entity_classes(*entity_classes)

    @property
    def QueryRoot(self):
        return self._build_root_type(
            "QueryRoot", "query_classes", self.schema.DEFAULT_QUERIES
        )

    @property
    def MutationRoot(self):
        return self._build_root_type(
            "MutationRoot", "mutation_classes", self.schema.DEFAULT_MUTATIONS
        )

    def _build_root_type(
        self, type_name, root_type_classes_key, root_type_classes_default
    ):
        attrs = {}
        for model_class in self.registry.available_model_classes:
            entity_class = self.registry.get_entity_class(model_class)

            # Add the query/mutation fields to the root type being built.
            root_types = getattr(entity_class, root_type_classes_key)

            # If the Entity class does not override query_classes or mutation_classes,
            # then we use the DEFAULT_QUERIES or DEFAULT_MUTATIONS from the schema.
            if root_types is None:
                root_types = root_type_classes_default

            for root_type in root_types:
                # Check permissions before we add the query/mutation type to the root.
                # E.g. insertFoo requires CREATE permission, so we only want to
                # define the insertFoo operation if the FooEntity has a Create in
                # its access_permissions field.
                root_type_permissions = root_type.get_required_access_permissions()
                if not entity_class.allows_permissions(root_type_permissions):
                    continue

                attrs.update(root_type.get_root_fields(self.registry, model_class))

        return type(type_name, (ObjectType,), attrs)
