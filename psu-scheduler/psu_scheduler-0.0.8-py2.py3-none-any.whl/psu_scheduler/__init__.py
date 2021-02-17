from django.conf import settings
from psu_base.classes.Log import Log
log = Log()

__version__ = '0.0.8'

__all__ = []

# Default settings
_DEFAULTS = {
    'SCHEDULER_PUBLIC_URLS': ['.*/scheduler/run', '.*/scheduler/aws/run', '.*/scheduler/test'],
    # Admin Menu Items
    'PSU_scheduler_ADMIN_LINKS'.upper(): [
        {
            'url': "scheduler:jobs", 'label': "Scheduled Jobs", 'icon': "fa-clock-o",
            'authorities': "DynamicPowerUser"
        },
        {
            'url': "scheduler:endpoints", 'label': "Schedule-able Endpoints", 'icon': "fa-link",
            'authorities': "DynamicPowerUser"
        },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_scheduler")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
