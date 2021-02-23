# noinspection PyUnresolvedReferences
import uuid

# noinspection PyUnresolvedReferences
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    x_edition = models.IntegerField(db_column='x_Edition', default=1)
    x_status = models.SmallIntegerField(db_column='x_Status', default=1)

    class Meta:
        abstract = True
