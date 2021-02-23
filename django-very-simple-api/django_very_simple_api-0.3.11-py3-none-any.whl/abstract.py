from django.db import models
from .serialize import Serialize


class SerializableQuerySet(models.QuerySet):
    def serialize(self, fields=None):
        return Serialize().serialize(qs=self, fields=fields)


class SerializableModel(models.Model):

    objects = models.Manager()
    serializable = SerializableQuerySet.as_manager()

    @property
    def serializable_fields(self):
        return []

    def serialize(self, fields=None):
        return Serialize().serialize(qs=self, fields=fields)

    class Meta:
        abstract = True
