from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kitchenart.log.signal import user_activity_log
from kitchenart.utils.broker import EventType


class LogViewSetMixin(ModelViewSet):
    entity = None

    def get_log_serializer_class(self):
        return self.get_serializer_class()

    def get_log_serializer(self, *args, **kwargs):
        log_serializer_class = self.get_log_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return log_serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        # send log signal
        if not request.user.is_anonymous:
            data_new = self.get_log_serializer(instance, context={'request': request}).data
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.created,
                                   entity=self.entity,
                                   instance_old=None,
                                   instance_new=data_new)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_old = deepcopy(instance)

        result = super().update(request, *args, **kwargs)

        # send log signal
        if not request.user.is_anonymous:
            # data old
            data_old = self.get_log_serializer(instance_old, context={'request': request}).data

            # data new
            data_new = self.get_log_serializer(self.get_object(), context={'request': request}).data
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.changed,
                                   entity=self.entity,
                                   instance_old=data_old,
                                   instance_new=data_new)

        return result

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # send log signal
        if not request.user.is_anonymous:
            serializer = self.get_log_serializer(instance, context={'request': request})
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.deleted,
                                   entity=self.entity,
                                   instance_old=serializer.data,
                                   instance_new=None)

        return Response(status=status.HTTP_204_NO_CONTENT)
