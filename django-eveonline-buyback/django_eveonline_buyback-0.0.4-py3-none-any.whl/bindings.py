from django.apps import apps 
from django.urls import reverse
from django.conf import settings
from .models import BuybackSettings
from .forms import EveBuybackSettingsForm
from packagebinder.bind import PackageBinding, SettingsBinding, TaskBinding, SidebarBinding
import logging 

logger = logging.getLogger(__name__)

app_config = apps.get_app_config('django_eveonline_buyback')

package_binding = PackageBinding(
    package_name=app_config.name, 
    version=app_config.version, 
    url_slug='eveonline', 
)

settings_binding = SettingsBinding(
    package_name=app_config.name, 
    settings_class=BuybackSettings,
    settings_form=EveBuybackSettingsForm,
)

sidebar_binding = SidebarBinding(
    package_name=app_config.name,
    parent_menu_item={
        "fa_icon": 'fa-store',
        "name": "Buyback",
        "url": reverse('django-eveonline-buyback'), 
    },
    child_menu_items=[]
)

def create_bindings():
    try:
        package_binding.save()
        settings_binding.save()
        sidebar_binding.save()
    except Exception as e:
        if settings.DEBUG:
            raise(e)
        else:
            logger.error(f"Failed package binding step for {app_config.name}: {e}")
