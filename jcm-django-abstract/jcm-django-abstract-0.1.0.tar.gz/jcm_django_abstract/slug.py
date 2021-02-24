from django.db import models
from autoslug import AutoSlugField


class AbstractUniqueNameSlug(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
