from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission


class ProjectPermissions(BasePermission):
    perms_map = {
        'DELETE': ['projects.change_project'],
        'GET': ['projects.view_project'],
        'HEAD': [],
        'OPTIONS': [],
        'POST': ['projects.change_project'],
    }

    def has_permission(self, request, view):
        if request.method not in self.perms_map:
            return MethodNotAllowed(request.method)

        if request.method == 'GET' and view.detail is True:
            return MethodNotAllowed(request.method)

        perms = self.perms_map[request.method]

        return request.user.has_perms(perms) or request.user.has_perms(perms, view.project)
