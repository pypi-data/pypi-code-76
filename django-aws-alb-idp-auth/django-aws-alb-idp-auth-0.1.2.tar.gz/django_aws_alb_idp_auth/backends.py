from django.contrib.auth.backends import RemoteUserBackend


class CreateUsperUserBackend(RemoteUserBackend):
    def configure_user(self, request, user):
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
