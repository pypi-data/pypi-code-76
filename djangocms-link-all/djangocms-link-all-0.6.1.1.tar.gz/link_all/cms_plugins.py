import logging
import os
from typing import List
from typing import Optional

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from dataclasses import dataclass
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.utils.translation import gettext as _

from link_all.models import LinkAllPluginModel
from link_all.models import LinkButtonPluginModel
from link_all.settings import LINK_ALL_ENABLE_BUTTON_PLUGIN


logger = logging.getLogger(__name__)


@dataclass
class SelectableModelInstance:
    pk: int
    label: str
    url: Optional[str]
    is_show_url_in_select: bool


@dataclass
class SelectableModel:
    content_type_pk: int
    verbose_name: str
    instances: List[SelectableModelInstance]


class LinkAllPlugin(CMSPluginBase):
    module = _("Generic")
    name = _("Link")
    model = LinkAllPluginModel
    render_template = 'link_all/link_all.html'
    text_enabled = True
    change_form_template = 'link_all/admin/link_all.html'

    fieldsets = [
        (None, {
            'fields': [
                'link',
                'link_type',
                'link_content_type',
                'link_instance_pk',
                'link_url',
                'link_label',
                'link_is_open_in_new_tab',
            ],
        }),
    ]

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['IS_LINK_ALL_DEV'] = os.environ.get('IS_LINK_ALL_DEV')
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_readonly_fields(self, request: HttpRequest, obj: LinkAllPluginModel = None) -> List[str]:
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('link',)

    def link(self, _) -> str:
        return ''

    def changeform_view(self, request, object_id: int = None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            extra_context['content_type'] = ContentType.objects.get_for_model(
                self.model.objects.get(pk=object_id)
            )
        return super().changeform_view(request, object_id, form_url, extra_context)


class LinkButtonPlugin(LinkAllPlugin):
    name = _("Link / Button")
    model = LinkButtonPluginModel
    render_template = 'link_all/link_all_button.html'
    fieldsets = [
        (None, {
            'fields': [
                'link',
                'link_type',
                'link_content_type',
                'link_instance_pk',
                'link_url',
                'link_label',
                'link_is_open_in_new_tab',
            ],
        }),
        ("Button configuration", {
            'fields': [
                'link_is_button',
                'link_button_color',
                'link_is_button_full_width',
                'link_is_button_outlined',
            ],
        }),
    ]


if LINK_ALL_ENABLE_BUTTON_PLUGIN:
    plugin_pool.register_plugin(LinkButtonPlugin)
else:
    plugin_pool.register_plugin(LinkAllPlugin)
