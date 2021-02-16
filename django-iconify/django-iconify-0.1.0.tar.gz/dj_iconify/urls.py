from django.urls import path, re_path

from . import views

urlpatterns = [
    path("_config.js", views.ConfigView.as_view(), name="config.js"),
    path("collection/", views.CollectionView.as_view(), name="collection"),
    path("collections/", views.CollectionsView.as_view(), name="collections"),
    re_path(
        r"^(?P<collection>[A-Za-z0-9-]+)\.(?P<format_>js(on)?)",
        views.IconifyJSONView.as_view(),
        name="iconify_json",
    ),
    re_path(
        r"^(?P<collection>[A-Za-z0-9-]+)/(?P<name>[A-Za-z0-9-]+)\.svg",
        views.IconifySVGView.as_view(),
        name="iconify_svg",
    ),
]
