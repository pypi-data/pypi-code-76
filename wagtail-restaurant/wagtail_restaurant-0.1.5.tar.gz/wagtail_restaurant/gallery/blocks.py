from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock

class InstagramBlock(blocks.StructBlock):
    instagram = blocks.ListBlock(blocks.StructBlock([('embed', EmbedBlock()),]))

    class Meta: 
        template = "gallery/blocks/instagram_block.html"
        icon = "cogs"
        label = "Instagram Images"