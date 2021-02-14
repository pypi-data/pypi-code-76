from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^visma_pay/callback/(?P<organizer_id>\d+)/(?P<payment_id>\d+)/', views.visma_pay_callback, name='visma_pay_callback'),
]
