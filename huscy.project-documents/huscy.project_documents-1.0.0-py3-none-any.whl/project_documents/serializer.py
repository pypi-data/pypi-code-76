from rest_framework import serializers

from huscy.project_documents import models, services


class DocumentSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)

    class Meta:
        model = models.Document
        fields = (
            'creator',
            'document_type',
            'document_type_name',
            'filehandle',
            'filename',
            'project',
            'uploaded_at',
            'uploaded_by',
        )
        read_only_fields = 'creator', 'filename', 'uploaded_at', 'uploaded_by'

    def create(self, validated_data):
        return services.create_document(**validated_data)


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = (
            'id',
            'name',
        )
