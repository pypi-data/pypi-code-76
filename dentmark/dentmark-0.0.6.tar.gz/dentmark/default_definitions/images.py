from dentmark import TagDef

class Image(TagDef):
    tag_name = 'img'
    # NOTE title already defined in anchor.TitleContext.
    # We can just re-use this context tag here since it has
    # the same configuration
    allow_children = ['title', 'alt']

    def render_main(self):
        # use first child as src
        # TODO better validation to enforce that this tag should have one
        # and only one TextNode child?
        src = self.content

        attrs = ''
        for ctx in ('title', 'alt'):
            ctx_val = self.context.get(ctx)
            if ctx_val:
                attrs += f' {ctx}="{ctx_val}"'

        return f'<img src="{src}"{attrs} />'

class AltContext(TagDef):
    tag_name = 'alt'
    is_context = True
    allow_children = []
