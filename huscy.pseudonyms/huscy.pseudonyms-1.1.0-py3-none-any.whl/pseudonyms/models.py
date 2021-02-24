from django.contrib.contenttypes.models import ContentType
from django.db import models

from huscy.subjects.models import Subject


class Pseudonym(models.Model):
    code = models.CharField(primary_key=True, max_length=64)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField(null=True)
