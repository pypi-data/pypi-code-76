from django.conf import settings
from django.db import models

from huscy.projects.models import Project


class DocumentType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Document(models.Model):
    def get_upload_path(self, filename):
        return f'documents/{filename}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    filehandle = models.FileField(upload_to=get_upload_path)
    filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
