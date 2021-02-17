from rest_framework.viewsets import ModelViewSet as DrfModelViewSet
from rest_framework.response import Response
from rest_framework import status


class ModelViewSet(DrfModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
