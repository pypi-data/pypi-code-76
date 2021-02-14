from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = '0.3.1'


class PluginApp(PluginConfig):
    name = 'pretix_bambora_payform'
    verbose_name = 'Visma Pay'

    class PretixPluginMeta:
        name = 'Visma Pay'
        author = 'Jaakko Rinta-Filppula'
        description = gettext_lazy('Payment plugin for Visma Pay')
        visible = True
        version = __version__
        category = 'PAYMENT'
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_bambora_payform.PluginApp'
