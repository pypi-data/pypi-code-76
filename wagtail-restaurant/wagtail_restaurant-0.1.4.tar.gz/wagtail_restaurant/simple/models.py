from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from .blocks import PageHeroBlock, UberUnsBlock, ImpressumBlock

import pathlib
resolve_path = pathlib.Path(__file__).resolve().parent # Resolve current directory for template

class SimplePage(Page):
    
    template = 'simple/simple_page.html'
    body = RichTextField(blank=True)
    hero = StreamField([("page_hero", PageHeroBlock())],null=True,blank=True,)
    impressum = StreamField([("menu", ImpressumBlock())], null=True, blank=True)
    uber_uns = StreamField([("menu", UberUnsBlock())], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        StreamFieldPanel("hero"),
        StreamFieldPanel("uber_uns"),
        StreamFieldPanel("impressum"),
    ]


    class Meta:  # noqa
        verbose_name = "Simple Page"
        verbose_name_plural = "Simple Pages"


 