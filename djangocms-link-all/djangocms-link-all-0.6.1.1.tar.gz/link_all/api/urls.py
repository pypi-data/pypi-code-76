from django.urls import path

from link_all.api.views import link_type_detail_view
from link_all.api.views import link_type_list_view


urlpatterns = [
    path('link-types/<int:pk>/', link_type_detail_view),
    path('link-types/', link_type_list_view),
]
