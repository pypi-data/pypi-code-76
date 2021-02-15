from dentmark import TagDef

class YouTubeEmbed(TagDef):
    tag_name = 'youtube'
    allow_children = ['width', 'height']

    def render_main(self):
        # TODO better validation to enforce that this tag should have one
        # and only one TextNode child?
        video_id = self.content

        src = f'https://www.youtube.com/embed/{video_id}'

        # TODO better validation to enforce that optional width/height
        # context is valid int
        width = self.context.get('width') or 560
        height = self.context.get('height') or 315

        return f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>'

class WidthContext(TagDef):
    tag_name = 'width'
    is_context = True
    allow_children = []

class HeightContext(WidthContext):
    tag_name = 'height'
