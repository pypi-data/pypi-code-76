from rest_framework.permissions import BasePermission


class ChangeSubjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('subjects.change_subject')


class ViewSubjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated and request.user.has_perm('subjects.view_subject')
        return True
