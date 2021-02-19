from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from .blocks import InstagramBlock

import pathlib
resolve_path = pathlib.Path(__file__).resolve().parent # Resolve current directory for template


class GalleryPage(Page):
    template = "gallery/gallery_page.html"
    instagram = StreamField([("instagram", InstagramBlock()),],null=True,blank=True,)

    content_panels = Page.content_panels + [StreamFieldPanel("instagram"),]
    class Meta:
        verbose_name = "Gallery Page"
        verbose_name_plural = "Gallery Pages"