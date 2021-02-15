"""test URLconf
"""
from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wagtail/', include(wagtailadmin_urls)),
]
