from django.conf import settings
from django.urls import path

from authens import conf as default_conf, views

app_name = "authens"
urlpatterns = [
    path("login/choose", views.LoginSwitchView.as_view(), name="login"),
    path("login/cas", views.CASLoginView.as_view(), name="login.cas"),
    path("login/pwd", views.PasswordLoginView.as_view(), name="login.pwd"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("reset/pwd", views.PasswordResetView.as_view(), name="reset.pwd"),
    path(
        "reset/pwd/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="reset.pwd.confirm",
    ),
]

if getattr(settings, "AUTHENS_USE_OLDCAS", default_conf.AUTHENS_USE_OLDCAS):
    urlpatterns += (
        path("login/oldcas", views.OldCASLoginView.as_view(), name="login.oldcas"),
    )
