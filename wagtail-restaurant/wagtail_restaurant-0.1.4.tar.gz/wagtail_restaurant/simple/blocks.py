from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.templatetags.wagtailcore_tags import richtext

class PageHeroBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:  # noqa
        template = "simple/blocks/hero.html"
        icon = "edit"
        label = "Page Hero"


class UberUnsBlock (blocks.StructBlock):
    content = blocks.RichTextBlock(required=False, help_text="Add additional content")

    class Meta:  # noqa
        template = "simple/blocks/uber_uns.html"
        icon = "placeholder"
        label = "Impressum"



class ImpressumBlock (blocks.StructBlock):
    content = blocks.RichTextBlock(required=False, help_text="Add additional content")

    class Meta:  # noqa
        template = "simple/blocks/impressum.html"
        icon = "placeholder"
        label = "Impressum"













