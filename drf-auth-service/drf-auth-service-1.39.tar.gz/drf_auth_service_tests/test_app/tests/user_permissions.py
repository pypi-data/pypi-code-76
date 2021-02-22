from rest_framework.permissions import IsAuthenticated

from drf_auth_service.common.permissions import ServiceTokenPermission

USER_PERMISSIONS = dict(set_password=[ServiceTokenPermission, IsAuthenticated])
