from rest_framework.permissions import BasePermission
from django.conf import settings
import os
from django.contrib.auth import get_user_model


class IPWhitelistMixin:

    def _has_permission(self, request):

        if os.getenv('GAE_APPLICATION', None):
            x_forwarded_for = request.META['HTTP_X_FORWARDED_FOR']
            i = x_forwarded_for.find(',')
            user_ip = x_forwarded_for[:i]
        else:
            user_ip = request.META['REMOTE_ADDR']

        for allow_ip in settings.IP_WHITELIST:
            if user_ip == allow_ip or user_ip.startswith(allow_ip):
                return True

        return False


class IsOwnerMixin:

    def _has_object_permission(self, request, obj):

        if request.user and request.user.is_authenticated:
            if isinstance(obj, get_user_model()):
                return obj == request.user
            else:
                return obj.user == request.user
        else:
            return False


class IsIPWhitelist(IPWhitelistMixin, BasePermission):

    def has_permission(self, request, view):
        return self._has_permission(request)


class IsOwnerOrIPWhitelist(IPWhitelistMixin, IsOwnerMixin, BasePermission):
    """Обьект принадлежит пользователю или запрос пришел с белого листа"""

    def has_object_permission(self, request, view, obj):

        if self._has_object_permission(request, obj) or self._has_permission(request):
            return True
        else:
            return False
