from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView as TamarinRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TamarinTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['pk'] = user.pk
        token['first-name'] = user.first_name
        token['last-name'] = user.last_name
        token['full-name'] = user.get_full_name()
        token['email'] = user.email
        token['username'] = user.username
        token['last-login'] = str(user.last_login)
        token['firebase-token'] = getattr(user, 'firebase_token', '')
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        token['groups'] = [group.name for group in user.groups.all()]
        token['permissions'] = [permission.split('.')[1] for permission in user.get_all_permissions()]
        return token


class TamarinTokenObtainPairView(TokenObtainPairView):
    serializer_class = TamarinTokenSerializer
