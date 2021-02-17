from .models import Report
from rest_framework.serializers import ModelSerializer


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
