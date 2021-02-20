from django.urls import path
from django_eveonline_buyback import views

urlpatterns = [
    path('buyback/', views.buyback, name="django-eveonline-buyback")
]
