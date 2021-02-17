class TypeRegistry:

    _ENTITY_CLASS_KEY = "__entity_class__"

    def __init__(self, schema):
        self.schema = schema
        self._schema_builder_mapping = schema.get_builder_mapping()
        self._node_graphql_type_name_to_model_class = {}
        self._cache = {
            "models": {},
            "types": {},
        }

    @property
    def available_model_classes(self):
        return self._model_cache.keys()

    @property
    def _model_cache(self):
        return self._cache["models"]

    @property
    def _type_cache(self):
        return self._cache["types"]

    def get_entity_class(self, model_class):
        return self._model_cache.get(model_class, {}).get(self._ENTITY_CLASS_KEY)

    def get_builder_class(self, type_key):
        return self._schema_builder_mapping[type_key]

    def lambda_from_registry(self, model_class, key):
        def _get_type_from_registry():
            cache_key = "{}/{}".format(model_class.__name__, key)
            if cache_key not in self._type_cache:
                raise RuntimeError(
                    "{} does not exist in DjraphQL type cache.".format(cache_key)
                )

            return self._type_cache[cache_key]

        return _get_type_from_registry

    def register_entity_classes(self, *entity_classes):
        # Entity classes for API settings
        for entity_class in entity_classes:
            model_class = entity_class.Meta.model

            self._cache["models"][model_class] = {
                self._ENTITY_CLASS_KEY: entity_class,
            }

            # Update our mapping of names (of GraphQL schema objects) to
            # model class and entity class. During query optimization,
            # as we traverse the tree of selected fields in the GraphQL query,
            # we only have access to the GraphQL type names. This mapping
            # will enable us to map those names to the associated model.
            node_name = self.schema.get_node_name_for_model(model_class)
            self._node_graphql_type_name_to_model_class[node_name] = {
                "model_class": model_class,
                "entity_class": entity_class,
            }

    def get_or_create_type(self, type_key, **kwargs):
        if type_key not in self._schema_builder_mapping:
            raise Exception(
                "get_or_create_type called with unknown key: {}".format(type_key)
            )

        # Check to see if we've already built this type and if so, return it.
        builder = self.get_builder_class(type_key)
        cache_key = builder.cache_key(type_key, **kwargs)
        if cache_key in self._type_cache:
            return self._type_cache[cache_key]

        # The type was not in the cache, so use the builder class
        # for this type key to create it, then cache the result and return it.
        result = builder.make(self, type_key=type_key, **kwargs)
        self._type_cache[cache_key] = result
        return result
