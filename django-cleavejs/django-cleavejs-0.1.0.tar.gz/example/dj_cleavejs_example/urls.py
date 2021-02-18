from django.urls import path

from .views import TestView

urlpatterns = [
    path("test.html", TestView.as_view()),
]
