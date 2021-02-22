from drf_auth_service.common.permissions import ServiceTokenPermission, SecretServiceTokenPermission

USER_PERMISSIONS = dict(
    user_confirm=[ServiceTokenPermission],
    resend_confirmation=[SecretServiceTokenPermission],
    destroy=[SecretServiceTokenPermission],
    block_user=[SecretServiceTokenPermission],
    list=[SecretServiceTokenPermission],
    unblock_user=[SecretServiceTokenPermission],
    default=[SecretServiceTokenPermission]
)
