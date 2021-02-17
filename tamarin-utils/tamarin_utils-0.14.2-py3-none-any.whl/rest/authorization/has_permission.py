from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.db.models import Q


class HasPermission(BasePermission):

    def has_permission(self, request, view):
        permissions = getattr(self, 'filter')
        if permissions:
            if type(permissions) == list:
                user_permissions = request.user.get('permissions')
                for permission in permissions:
                    if not (permission in user_permissions):
                        return False
                return True
            elif type(permissions) == str:
                return bool(permissions in request.user.get('permissions'))
            else:
                raise AttributeError('permissions type is not list or string')
        else:
            raise AttributeError('permissions does not set')


class HasUserPermission(BasePermission):

    def has_permission(self, request, view):
        User = get_user_model()
        permissions = getattr(self, 'filter')
        if permissions:
            if type(permissions) == list:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(user_permissions__codename__in=permissions) | Q(groups__permissions__codename__in=permissions),
                )
                return queryset.exists()
            elif type(permissions) == str:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(user_permissions__codename=permissions) | Q(groups__permissions__codename=permissions),
                )
                return queryset.exists()
            else:
                raise AttributeError('permissions type is not list or string')
        else:
            raise AttributeError('permissions does not set')
