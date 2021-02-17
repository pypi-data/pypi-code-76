from .serializer import ReportSerializer
from .models import Report
from tamarin.rest.viewset import ReadOnlyModelViewSet
from rest_framework_api_key.permissions import HasAPIKey


class ReportApi(ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [HasAPIKey, ]
