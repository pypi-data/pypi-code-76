from django.conf.urls import url

from . import views

urlpatterns = [
    url('^/(.+)$', views.StaticFilesList(), name='papyru_static_files'),
]
