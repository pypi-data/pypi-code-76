"""django adapter."""

from django.conf import settings
settings_file = settings.BUCKET_ADAPTER_SETTING
from adapter import Adapter

genric_adapter = Adapter(settings_file)
