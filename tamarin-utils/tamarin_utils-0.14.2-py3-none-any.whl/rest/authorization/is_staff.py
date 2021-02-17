from rest_framework import permissions


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        is_not_anonymous = str(request.user) != 'AnonymousUser'
        return is_not_anonymous and request.user.get('is_active') and request.user.get('is_staff')


class IsUserStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        is_not_anonymous = str(request.user) != 'AnonymousUser'
        is_active = request.user.is_active
        is_staff = request.user.is_staff
        return is_not_anonymous and is_active and is_staff
