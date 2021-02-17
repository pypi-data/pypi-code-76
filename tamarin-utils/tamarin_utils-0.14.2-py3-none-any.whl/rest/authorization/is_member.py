from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.db.models import Q


class IsMember(BasePermission):

    def has_permission(self, request, view):
        groups = getattr(self, 'filter')
        if groups:
            if type(groups) == list:
                user_groups = request.user.get('groups')
                for group in groups:
                    if not (group in user_groups):
                        return False
                return True
            elif type(groups) == str:
                return groups in request.user.get('groups')
            else:
                raise AttributeError('groups type is not list or string')
        else:
            raise AttributeError('groups does not set')


class IsUserMember(BasePermission):

    def has_permission(self, request, view):
        User = get_user_model()
        groups = getattr(self, 'filter')
        if groups:
            if type(groups) == list:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(groups__name__in=groups)
                )
                return queryset.exists()
            elif type(groups) == str:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(groups__name=groups)
                )
                return queryset.exists()
            else:
                raise AttributeError('groups type is not list or string')
        else:
            raise AttributeError('groups does not set')
