from django.conf import settings
from dateutil import tz

ALLOWED_STATUS = getattr(settings, 'LAMAGRAM_ALLOWED_STATUS', [])
ALLOWED_ALL = getattr(settings, 'LAMAGRAM_ALLOWED_ALL', False)
