from django.urls import path
from . import views

urlpatterns = [
    path('getServerSettings', views.getServerSettings),
    path('getScheduleSettings', views.getScheduleSettings),
    path('reportRunResult', views.reportRunResult),
]

