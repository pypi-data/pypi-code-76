from django_extensions.db.models import ActivatorModel
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from bitsoframework.notifications.serializers import DeviceSerializer


class DeviceViewMixin(object):

    @action(methods=["GET"], detail=False, url_path="devices")
    def list_devices(self, request):
        """
        Attach a new photo to the underlying record.
        """

        queryset = request.user.devices.active()

        serializer = DeviceSerializer(instance=queryset, many=True)

        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path="devices/save")
    def register_device(self, request):
        """
        Attach a new photo to the underlying record.
        """

        instance = request.user.devices.filter(token=request.data.get("token")).first()

        if instance:

            serializer = DeviceSerializer(data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)

            serializer.save(status=ActivatorModel.ACTIVE_STATUS)

            return Response(serializer.data, status=HTTP_200_OK)
        else:

            serializer = DeviceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user=request.user)

            return Response(serializer.data, status=HTTP_201_CREATED)
