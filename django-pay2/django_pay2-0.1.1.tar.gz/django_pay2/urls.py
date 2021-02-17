from django.urls import include, path

from . import views

app_name = "django_pay2"

urlpatterns = [
    path("success/", views.SuccessPaymentView.as_view(), name="success"),
    path("fail/", views.RejectedPaymentView.as_view(), name="fail"),
    path(
        "debug_payments/<uuid:pk>/",
        views.DebugPaymentView.as_view(),
        name="debug_payment",
    ),
    path(
        "debug_payments/<uuid:pk>/accept/",
        views.AcceptDebugPaymentView.as_view(),
        name="debug_accept",
    ),
    path(
        "debug_payments/<uuid:pk>/reject/",
        views.RejectDebugPaymentView.as_view(),
        name="debug_reject",
    ),
    path("tinkoff/", include("django_pay2.providers.tinkoff.urls")),
]
