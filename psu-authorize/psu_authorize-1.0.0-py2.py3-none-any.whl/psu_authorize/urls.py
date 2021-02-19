from django.urls import path
from . import views

urlpatterns = [
    # A simple test page
    path('', views.index, name='authorize_index'),
    path('app', views.index, name='app_list'),
    path('app/<str:app_code>/', views.app, name='authorize_app'),
    path('grant', views.grant, name='grant_permission'),
    path('revoke', views.revoke, name='revoke_permission_tbd'),
    path('revoke/<int:permission_id>/', views.revoke, name='revoke_permission')
]
