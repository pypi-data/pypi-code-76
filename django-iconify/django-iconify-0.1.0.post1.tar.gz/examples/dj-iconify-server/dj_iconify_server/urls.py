from django.views.generic import TemplateView
from django.urls import include, path

urlpatterns = [
    path("icons/", include("dj_iconify.urls")),
    path("test.html", TemplateView.as_view(template_name="test.html")),
]
