# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from .views import WebHookReceiverView

app_name = 'contentful_webhook_receiver'
urlpatterns = [
    url(r'^hook/$', WebHookReceiverView.as_view()),
]
