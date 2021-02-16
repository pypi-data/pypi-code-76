from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from terra_settings.settings import TERRA_APPLIANCE_SETTINGS


class SettingsView(APIView):
    """ This is public endpoint used to init terralego apps """
    permission_classes = (AllowAny, )

    def get(self, request):
        terra_settings = {
            # for the moment, language is fixed and defined by backend instance
            'language': settings.LANGUAGE_CODE.lower(),
        }

        if 'mapbox_baselayer' in settings.INSTALLED_APPS:
            from mapbox_baselayer.models import MapBaseLayer
            from terra_settings.base_layers.serializers import PublicMapBaseLayerSerializer

            terra_settings['base_layers'] = PublicMapBaseLayerSerializer(MapBaseLayer.objects.all(), many=True).data

        # always override terra_settings data with TERRA_APPLIANCE_SETTINGS content
        terra_settings.update(TERRA_APPLIANCE_SETTINGS)

        return Response(terra_settings)
