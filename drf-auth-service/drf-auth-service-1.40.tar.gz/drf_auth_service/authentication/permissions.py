from drf_auth_service.common.permissions import ServiceTokenPermission

AUTHENTICATION_PERMISSIONS = dict(
    register=[ServiceTokenPermission],
    send_reset_password=[ServiceTokenPermission],
    reset_password_confirm=[ServiceTokenPermission],
    default=[ServiceTokenPermission]
)
