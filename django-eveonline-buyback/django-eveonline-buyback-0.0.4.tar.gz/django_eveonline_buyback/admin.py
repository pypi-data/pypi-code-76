from django.contrib import admin
from django_eveonline_buyback.models import BuybackSettings
from django_singleton_admin.admin import DjangoSingletonModelAdmin


admin.site.register(BuybackSettings, DjangoSingletonModelAdmin)
