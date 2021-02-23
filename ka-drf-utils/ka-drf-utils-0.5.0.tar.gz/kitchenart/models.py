from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from gramedia.django.abstract_models import TimestampedModel


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(_('active'), default=True)
    deleted = models.DateTimeField(
        _('deleted'),
        blank=True,
        null=True,
        help_text=_('Date/time this object was deleted.')
    )

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return True if self.deleted else False

    def delete(self):
        self.is_active = False
        self.deleted = timezone.now()
        self.save()

    def restore(self):
        self.deleted = None
        self.save()


class BaseModel(SoftDeleteModel, TimestampedModel):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
