from django.db import models
from .tracking import AbstractDeleteTime
from .uuid import AbstractUUID
from .slug import AbstractUniqueNameSlug


class AbstractForeignKeySelect(AbstractUniqueNameSlug, AbstractDeleteTime, AbstractUUID):
    default_order = models.IntegerField(default=0)

    class Meta:
        abstract = True
