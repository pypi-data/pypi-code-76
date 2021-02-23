from django.urls import path, include

from .views import set_language

app_name = 'ok-language-tools'

urlpatterns = [
    path('language-tools/', include([
        path('set-language/', set_language, name='set-language')
    ]))
]
