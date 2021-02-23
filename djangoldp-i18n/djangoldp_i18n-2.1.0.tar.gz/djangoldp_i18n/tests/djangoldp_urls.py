from django.conf.urls import url
from djangoldp.permissions import LDPPermissions
from djangoldp_i18n.tests.models import MultiLingualModel, MultiLingualChild
from djangoldp_i18n.views import I18nLDPViewSet

urlpatterns = [
    url(r'^multilingualmodel/', I18nLDPViewSet.urls(
        model=MultiLingualModel, permission_classes=[LDPPermissions], nested_fields=['children'])),
    url(r'^multilingualchildren/', I18nLDPViewSet.urls(
        model=MultiLingualChild, permission_classes=[LDPPermissions], nested_fields=[])),
]
