from rest_framework import serializers

from terra_settings.tests.test_app.models import DummyModel


class DummySerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyModel
        fields = ('name', 'properties')
