from django.urls import path
from django.views.generic import TemplateView

from homepage import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', TemplateView.as_view(template_name='homepage/robots.txt', content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name='homepage/sitemap.xml', content_type='text/xml')),
]
