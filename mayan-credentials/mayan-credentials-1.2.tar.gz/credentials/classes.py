import logging

from django.utils import six
from django.utils.translation import ugettext_lazy as _

# Change this to mayan.apps.common.class_mixins for Mayan EDMS 3.5
from .compat import AppsModuleLoaderMixin

logger = logging.getLogger(name=__name__)

__all__ = ('CredentialBackend',)


class CredentialBackendMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == 'credentials.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class CredentialBackendBase(AppsModuleLoaderMixin):
    """
    Base class for the credential backends.

    The fields attribute is a list of dictionaries with the format:
    {
        'name': ''  # Field internal name
        'label': ''  # Label to show to users
        'initial': ''  # Field initial value
        'default': ''  # Default value.
    }

    """
    fields = {}

    @classmethod
    def get_class_fields(cls):
        backend_field_list = getattr(cls, 'fields', {}).keys()
        return getattr(cls, 'class_fields', backend_field_list)


class CredentialBackend(
    six.with_metaclass(CredentialBackendMetaclass, CredentialBackendBase)
):
    _loader_module_name = 'credential_backends'

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (
                    key, backend.label
                ) for key, backend in cls.get_all().items()
            ], key=lambda x: x[1]
        )


class NullBackend(CredentialBackend):
    label = _('Null backend')
