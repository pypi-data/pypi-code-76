from django.urls import path
from . import views

urlpatterns = [
    path('updateApiResponseTimeStats', views.updateApiResponseTimeStats),
]


