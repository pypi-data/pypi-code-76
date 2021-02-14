from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bambora/callback/(?P<organizer_id>\d+)/(?P<payment_id>\d+)/', views.bambora_callback, name='bambora_callback'),
]
