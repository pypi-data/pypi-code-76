"""djangoldp uploader URL Configuration"""

from django.conf import settings
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from djangoldp_energiepartagee import views
from djangoldp_energiepartagee.views import ContributionsCallView, ContributionsReminderView, ContributionsVentilationView

urlpatterns = [
    url(r'^contributions/call/$', csrf_exempt(ContributionsCallView.as_view()), name='contributions-call'),
    url(r'^contributions/reminder/$', csrf_exempt(ContributionsReminderView.as_view()), name='contributions-reminder'),
    url(r'^contributions/ventilation/$', csrf_exempt(ContributionsVentilationView.as_view()), name='contributions-ventilation'),
]
