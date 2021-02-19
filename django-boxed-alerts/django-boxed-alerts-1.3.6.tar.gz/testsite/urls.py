"""
Provide urls for the test site.
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from .views import Home

# pylint: disable=invalid-name
urlpatterns = []\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^alerts/', include('alerts.urls')),
    url(r'^$', Home.as_view(), name='home'),
]
