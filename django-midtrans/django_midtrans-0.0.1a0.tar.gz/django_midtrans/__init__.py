import midtransclient
from django.conf import settings
from django.utils.functional import SimpleLazyObject

# version
VERSION = (0, 0, '1a')
__version__ = ".".join(str(i) for i in VERSION)

default_app_config = "django_midtrans.apps.DjangoMidtransConfig"


# environments
MIDTRANS_SETTINGS_AVAILABLE = {
    'is_production': 'MIDTRANS_IS_PRODUCTION',
    'server_key': 'MIDTRANS_SERVER_KEY',
    'client_key': 'MIDTRANS_CLIENT_KEY'
}
MIDTRANS_DOCS = "https://github.com/Midtrans/midtrans-python-client"


# mixins
class DefaultSettingMixin:
    def __init__(self):
        self._default_settings = self.__check_default_settings(self.default_settings)
        super().__init__(**self._default_settings)

    @property
    def default_settings(self):
        if not hasattr(self, '_default_settings'):
            self._default_settings = {
                key: getattr(settings, value, '') for (key, value) in MIDTRANS_SETTINGS_AVAILABLE.items()
            }
        return self._default_settings

    def __check_default_settings(self, default_settings):
        for key, value in default_settings.items():
            if value == '':
                raise RuntimeError(
                    "The '%s' is not available on your settings. Please refer to '%s' how to set it." % (
                        MIDTRANS_SETTINGS_AVAILABLE[key], MIDTRANS_DOCS)
                )
        return default_settings


class CoreApiAdapter(DefaultSettingMixin, midtransclient.CoreApi):
    pass


class SnapAdapter(DefaultSettingMixin, midtransclient.Snap):
    pass


snap: SnapAdapter = SimpleLazyObject(lambda: SnapAdapter()) # noqa
core = CoreApiAdapter = SimpleLazyObject(lambda: CoreApiAdapter()) # noqa
