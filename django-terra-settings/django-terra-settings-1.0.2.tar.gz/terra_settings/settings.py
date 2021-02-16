from django.conf import settings

TERRA_APPLIANCE_SETTINGS = getattr(settings, 'TERRA_APPLIANCE_SETTINGS', {})
FRONT_URL = getattr(settings, 'FRONT_URL', 'http://localhost:3000')
HOSTNAME = getattr(settings, 'HOSTNAME', 'http://localhost:8000')

MEDIA_ACCEL_REDIRECT = getattr(settings, 'MEDIA_ACCEL_REDIRECT', False)
