from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from huscy.bookings import models, serializers, services
from huscy.projects.models import Project


class CanAddBookings(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('bookings.add_booking')


class CanDeleteBookings(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('bookings.delete_booking')


class TimeslotViewSet(viewsets.ModelViewSet):
    queryset = models.Timeslot.objects.all()
    serializer_class = serializers.TimeslotSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    def perform_destroy(self, timeslot):
        try:
            services.delete_timeslot(timeslot)
        except services.BookingExistsException as e:
            raise ValidationError(e)

    @action(detail=True, methods=['post'], permission_classes=[CanAddBookings])
    def book(self, request, pk):
        timeslot = self.get_object()
        try:
            services.book_timeslot(timeslot, "abc")
        except services.CannotBookInactiveTimeslotException as e:
            raise ValidationError(e)
        return Response(self.get_serializer(timeslot).data, status=HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[CanDeleteBookings])
    def unbook(self, request, pk):
        timeslot = self.get_object()
        services.unbook_timeslot(timeslot)
        return Response(status=HTTP_204_NO_CONTENT)


class ProjectViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Project.objects.all()

    @action(detail=True, methods=['get'])
    def timeslots(self, request, pk=None):
        project = self.get_object()
        timeslots = services.get_timeslots_for_project(project)
        return Response(data=serializers.TimeslotSerializer(timeslots, many=True).data)
