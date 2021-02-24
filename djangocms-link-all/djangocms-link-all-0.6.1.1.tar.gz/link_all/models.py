import logging

from cms.models import CMSPlugin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from enumfields import Enum
from enumfields import EnumField
from filer.models import File


logger = logging.getLogger(__name__)


class FilerFileLinkable(File):
    def get_absolute_url(self) -> str:
        return self.url

    class Meta(File.Meta):
        proxy = True


class LinkType(Enum):
    URL = 'url'
    EMAIL = 'email'
    PHONE = 'phone'
    ANCHOR = 'anchor'
    GENERIC_FOREIGN_KEY = 'generic_foreign_key'


class LinkAllMixin(models.Model):
    link_type = EnumField(LinkType, default=LinkType.URL, max_length=64)
    link_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    link_instance_pk = models.PositiveIntegerField(blank=True, null=True)
    link_instance = GenericForeignKey('link_content_type', 'link_instance_pk')
    link_url = models.CharField(max_length=1024, blank=True)
    link_label = models.CharField(max_length=1024, blank=True)
    link_is_open_in_new_tab = models.BooleanField(default=False, verbose_name="Open in a new tab")
    link_is_optional = False

    class Meta:
        abstract = True

    def is_link_empty(self) -> bool:
        return self.get_link_url() == ''

    def get_link_url(self) -> str:
        from link_all.api.views import get_link_instance_url
        from link_all.settings import LINK_ALL_MODELS

        if self.link_type == LinkType.GENERIC_FOREIGN_KEY:
            link_all_model_current = None
            for link_all_model in LINK_ALL_MODELS:
                if (
                    link_all_model.app_label == self.link_content_type.app_label and
                    link_all_model.model_name.lower() == self.link_content_type.model.lower()
                ):
                    link_all_model_current = link_all_model
            return get_link_instance_url(self.link_instance, link_all_model_current)
        elif self.link_type == LinkType.EMAIL:
            return f'mailto:{self.link_url}'
        elif self.link_type == LinkType.PHONE:
            return f'tel:{self.link_url}'
        elif self.link_type == LinkType.ANCHOR:
            return f'#{self.link_url}'
        elif self.link_url:
            return self.link_url
        else:
            return ''

    def get_link_label(self) -> str:
        if self.link_label:
            return self.link_label
        elif self.link_instance:
            return str(self.link_instance)
        elif self.link_url:
            return self.link_url
    
    def clean(self):
        if not self.link_is_optional:
            if self.link_content_type and not self.link_instance:
                raise ValidationError("This link type requires an object to be selected.")
            if self.link_type == LinkType.GENERIC_FOREIGN_KEY and not self.link_instance:
                raise ValidationError("This link type requires an object to be selected.")
            if self.link_type != LinkType.GENERIC_FOREIGN_KEY and not self.link_url:
                raise ValidationError("This link type requires a url to be specified.")

    def __str__(self) -> str:
        return link_str(self)


class ButtonColor(Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    WARNING = 'warning'
    SUCCESS = 'success'
    DANGER = 'danger'
    INFO = 'info'
    LIGHT = 'light'
    DARK = 'dark'


class LinkAllBootstrapButtonMixin(models.Model):
    link_is_button = models.BooleanField(default=False, verbose_name="Render as button")
    link_button_color = EnumField(
        ButtonColor,
        default=ButtonColor.PRIMARY,
        max_length=64,
        verbose_name="Color",
        blank=True,
    )
    link_is_button_full_width = models.BooleanField(default=False, verbose_name="Full width")
    link_is_button_outlined = models.BooleanField(default=False, verbose_name="Transparent body")

    class Meta:
        abstract = True


class LinkAllPluginModel(LinkAllMixin, CMSPlugin):
    pass


class LinkButtonPluginModel(LinkAllMixin, LinkAllBootstrapButtonMixin, CMSPlugin):
    pass


def link_str(link_obj: LinkAllMixin) -> str:
    if link_obj.link_type == LinkType.GENERIC_FOREIGN_KEY:
        if link_obj.link_instance:
            return f'{link_obj.link_instance._meta.verbose_name} - {link_obj.get_link_url()}'
        elif link_obj.link_label:
            return link_obj.link_label
    else:
        if link_obj.link_url:
            return link_obj.link_url
        else:
            return ''
