from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from .views import TokenView, UserDataView, GetStudentInfoView


schema_view = get_swagger_view(title='SSO API')

urlpatterns = [
	path('schema/', get_schema_view(
		title="Kodland SSO service",
		description="API for all things",
	), name='openapi-schema'),
	path('swagger', schema_view),
	path('token', TokenView.as_view(), name='token'),
	path('info', UserDataView.as_view(), name='user_info'),
	path('student_info', GetStudentInfoView.as_view(), name='student_info')
]
