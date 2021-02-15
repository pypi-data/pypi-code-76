from .anchor import Anchor, URLContext, TitleContext
from .annotation import Annotation, FootNote
from .headlines import H1, H2, H3, H4, H5, H6
from .emphasis import Italic, Bold, StrikeThrough
from .lists import OrderedList, UnorderedList, ListItem
from .tables import Table, TableRow, TableCell, ColspanContext, RowspanContext, AlignContext
from .images import Image, AltContext
from .youtube import YouTubeEmbed, WidthContext, HeightContext

from dentmark import TagDef

class Root(TagDef):
    tag_name = 'root'
    is_root = True
    exclude_children = [] # exclude nothing (allow everything)

    def render_main(self):
        body = f'{self.content}'

        fns = self.collectors.get('fn', [])
        fns_rendered = ''.join(fns)

        if fns_rendered:
            body += f'<section class="footnotes" role="doc-endnotes"><ol>{fns_rendered}</ol></section>'

        return body

class Pre(TagDef):
    tag_name = 'pre'
    is_pre = True

    def render_main(self):
        return f'<pre>{self.content}</pre>'

class Paragraph(TagDef):
    tag_name = 'p'
    exclude_children = ['p', 'li', 'bq']

    def render_main(self):
        return f'<p>{self.content}</p>'

class BlockQuote(TagDef):
    tag_name = 'bq'
    allow_children = ['p', 'b', 's', 'i'] # TODO probably some others too

    def render_main(self):
        return f'<blockquote>{self.content}</blockquote>'

class HorizontalRule(TagDef):
    tag_name = 'hr'
    allow_children = []

    #TODO maybe enforce that this can't have any text/children?
    def render_main(self):
        return '<hr/>'

class Break(TagDef):
    tag_name = 'br'
    allow_children = []

    #TODO maybe enforce that this can't have any text/children?
    def render_main(self):
        return '<br/>'


REGISTERED_TAGS = (
    Root,
    H1, H2, H3, H4, H5, H6,
    Anchor, URLContext, TitleContext,
    Pre,
    Paragraph,
    Annotation, FootNote,
    Italic, Bold, StrikeThrough,
    OrderedList, UnorderedList, ListItem,
    Table, TableRow, TableCell, ColspanContext, RowspanContext, AlignContext,
    BlockQuote,
    HorizontalRule,
    Break,
    Image, AltContext,
    YouTubeEmbed, WidthContext, HeightContext,
)
