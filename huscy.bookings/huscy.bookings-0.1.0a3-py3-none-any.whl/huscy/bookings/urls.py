from rest_framework.routers import DefaultRouter

from huscy.bookings import views


router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('timeslots', views.TimeslotViewSet)

urlpatterns = [
]

urlpatterns += router.urls
