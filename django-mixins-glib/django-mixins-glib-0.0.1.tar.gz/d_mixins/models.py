from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TimeStampMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # START SYSTEM DEFINED ---
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='%(class)s_modified_by')

    # END SYSTEM DEFINED ---
    class Meta:
        abstract = True
