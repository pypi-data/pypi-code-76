from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from jose import jwt
from django.contrib.auth import get_user_model
from django.conf import settings


class TamarinUserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        user = AnonymousUser()
        try:
            raw_token = str(request.headers['Authorization'])
            if not raw_token.startswith('Bearer'):
                return user, None
            net_token = raw_token.split(' ')
            if not len(net_token) == 2:
                return user, None
            token = net_token[1].strip()
            key = getattr(settings, 'TAMARIN_JWT_KEY', settings.SECRET_KEY)
            token = jwt.decode(token, key)
            user_queryset = User.objects.filter(pk=token['pk'])
            if token['token_type'] == 'access' and user_queryset.exists():
                user = user_queryset.last()
            return user, None
        except Exception as e:
            return user, None


class TamarinTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        user = AnonymousUser()
        try:
            raw_token = str(request.headers['Authorization'])
            if not raw_token.startswith('Bearer'):
                setattr(request, 'crs_client', None)
                return user, None
            net_token = raw_token.split(' ')
            if not len(net_token) == 2:
                setattr(request, 'crs_client', None)
                return user, None
            token = net_token[1].strip()
            key = getattr(settings, 'TAMARIN_JWT_KEY', settings.SECRET_KEY)
            token = jwt.decode(token, key)
            if token['token_type'] == 'access':
                setattr(request, 'crs_client', token)
                user = token
            else:
                setattr(request, 'crs_client', None)
            return user, None
        except Exception as e:
            setattr(request, 'crs_client', None)
            return user, None
