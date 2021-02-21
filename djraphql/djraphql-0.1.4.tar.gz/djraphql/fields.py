from graphene import Int, String
from djraphql.util.django_models import get_field_by_name


class ModelField:
    def __init__(self, name, read_only=False, graphene_type=None):
        self.name = name
        self.read_only = read_only
        self.graphene_type = graphene_type

    def get_graphene_type(self, model_class, type_mapping):
        if self.graphene_type:
            return self.graphene_type

        field = get_field_by_name(model_class, self.name)
        return self.graphene_type or type_mapping[field.get_internal_type()]

    def get_resolver(self, entity_class):
        return lambda context, instance: getattr(instance, self.name, None)

    def get_django_model_field(self, model_class):
        return get_field_by_name(model_class, self.name)


class ComputedField:
    def __init__(self, name, graphene_type):
        self.name = name
        self.graphene_type = graphene_type

    def get_graphene_type(self, model_class, type_mapping):
        return self.graphene_type

    def get_resolver(self, entity_class):
        def method_property_resolver(context, instance):
            resolver = getattr(entity_class, "get_{}".format(self.name))
            return resolver(context, instance)

        return method_property_resolver


class AllModelFields:
    def __init__(self, excluding=()):
        self.exclude_fields = excluding

    def field_is_excluded(self, field):
        return field.name in self.exclude_fields

    def generate_model_fields(self, model_class):
        return {
            field.name: ModelField(field.name)
            for field in model_class._meta.get_fields()
            if field.name not in self.exclude_fields
        }
