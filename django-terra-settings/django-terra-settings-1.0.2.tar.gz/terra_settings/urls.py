from django.conf import settings
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from terra_settings.views import SettingsView

router = SimpleRouter()

if 'mapbox_baselayer' in settings.INSTALLED_APPS:
    from terra_settings.base_layers.views import BaseLayerViewSet
    # enable mapbox_baselayer related endpoints if module enabled in backend
    router.register('baselayer', BaseLayerViewSet, basename='baselayer')

urlpatterns = [
    # public api view
    path('settings/', SettingsView.as_view(), name='settings'),
    # router urls
    path('', include(router.urls)),
]
