import math

from django.conf import settings


class WoolsSettings:
    """
    Proxy over the Django settings to provide defaults (and shortcuts)
    """

    _defaults = dict(
        MAX_PIXEL_RATIO=3.0, INCREMENT_STEP_PERCENT=(math.sqrt(2) - 1) * 100,
    )

    def __getattr__(self, item):
        return getattr(settings, f"WOOL_{item}", self._defaults[item])


wool_settings = WoolsSettings()
