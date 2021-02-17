from djraphql.access_permissions import (
    CREATE,
    READ,
    UPDATE,
    DELETE,
    R,
    AccessPermissionsBitmap,
)
from djraphql.fields import AllModelFields, ComputedField, ModelField


class Entity:
    properties = ()
    filter_backends = ()
    access_permissions = (R,)
    query_classes = None
    mutation_classes = None
    validator = None

    @classmethod
    def get_queryset(cls, context):
        queryset = cls.Meta.model.objects.all()

        try:
            for backend_filter in cls.filter_backends:
                queryset = backend_filter.filter_backend(context, queryset)
        except Exception as e:
            raise Exception(
                "An error occurred when applying filter backend {}: {}".format(
                    backend_filter.__class__.__name__, str(e)
                )
            )

        return queryset

    @classmethod
    def can_get_for_insert(cls):
        return cls.get_for_insert != Entity.get_for_insert

    @staticmethod
    def get_for_insert(context):
        raise NotImplementedError()

    @classmethod
    def allows_permissions(cls, access_permissions):
        """Check that the access_permissions field defined on this Entity class
        matches the passed in access_permissions bitmap, which will come from
        AbstractRootTypeBuilder.get_required_access_permissions().

        This check is generally used to ensure we want to expose a Root query
        or mutation for an Entity, e.g. fooByPk should only exist if FooEntity's
        READ flag is 1.
        """
        return access_permissions == (
            cls._get_access_permissions_bitmap() & access_permissions
        )

    @classmethod
    def is_creatable(cls):
        return bool(cls._get_access_permissions_bitmap() & CREATE)

    @classmethod
    def is_readable(cls):
        return bool(cls._get_access_permissions_bitmap() & READ)

    @classmethod
    def is_updatable(cls):
        return bool(cls._get_access_permissions_bitmap() & UPDATE)

    @classmethod
    def is_deletable(cls):
        return bool(cls._get_access_permissions_bitmap() & DELETE)

    @classmethod
    def is_creatable_by_context(cls, context):
        return cls._is_context_authorized_for_permission_type(context, CREATE)

    @classmethod
    def is_readable_by_context(cls, context):
        return cls._is_context_authorized_for_permission_type(context, READ)

    @classmethod
    def is_updatable_by_context(cls, context):
        return cls._is_context_authorized_for_permission_type(context, UPDATE)

    @classmethod
    def is_deletable_by_context(cls, context):
        return cls._is_context_authorized_for_permission_type(context, DELETE)

    @classmethod
    def _is_context_authorized_for_permission_type(cls, context, permission_type):
        for access_permission in cls.access_permissions:
            if access_permission.matches(permission_type):
                return access_permission.has_permission(context)

        return False

    @classmethod
    def _get_access_permissions_bitmap(cls):
        # Cache the AccessPermissionsBitmap and reuse it across calls
        if not hasattr(cls, "_access_permissions_bitmap"):
            cls._access_permissions_bitmap = AccessPermissionsBitmap(
                *cls.access_permissions
            )
        return cls._access_permissions_bitmap

    @staticmethod
    def before_insert(data, context):
        pass

    @classmethod
    def _get_meta_fields(cls):
        return getattr(cls.Meta, "fields", ())

    @classmethod
    def _field_is_excluded_or_not_included(cls, field):

        (
            basic_fields,
            computed_fields,
            special_fields,
        ) = cls._partition_basic_and_special_fields()

        # Is there a ModelField instance for this field? If so, it's not excluded.
        if any(f.name == field.name for f in basic_fields):
            return False

        # Is there an AllModelFields?
        all_models_fields = [f for f in special_fields if isinstance(f, AllModelFields)]
        if all_models_fields:
            # Is the field on the AllModelFields's exclusion list?
            return field.name in all_models_fields[0].exclude_fields

        return True

    @classmethod
    def _get_computed_fields(cls):
        return [f for f in cls._get_meta_fields() if isinstance(f, ComputedField)]

    @classmethod
    def _get_model_fields(cls):
        return [f for f in cls._get_meta_fields() if isinstance(f, ModelField)]

    @classmethod
    def _partition_basic_and_special_fields(cls):
        fields_list = cls._get_meta_fields()
        special_fields = []
        computed_fields = []
        basic_fields = []

        for field in fields_list:
            if isinstance(field, AllModelFields):
                special_fields.append(field)
            elif isinstance(field, ComputedField):
                computed_fields.append(field)
            else:
                basic_fields.append(field)

        assert len(special_fields) <= 1, "Provide zero or one AllModelFields instances."
        return basic_fields, computed_fields, special_fields

    @classmethod
    def _field_is_read_only(cls, field):
        return any(
            f.name == field.name and f.read_only for f in cls._get_model_fields()
        )
