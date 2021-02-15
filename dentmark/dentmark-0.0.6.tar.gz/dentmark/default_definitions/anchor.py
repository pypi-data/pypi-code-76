from dentmark import TagDef

class Anchor(TagDef):
    tag_name = 'a'
    allow_children = ['url', 'title', 'i', 'b', 's']

    def render_main(self):
        url = self.context.get('url')
        if url is None:
            if self.content.startswith('http'):
                url = self.content

        href = f' href="{url}"' if url else ''

        title = self.context.get('title')
        title_str = f' title="{title}"' if title else ''

        return f'<a{href}{title_str}>{self.content}</a>'

class URLContext(TagDef):
    tag_name = 'url'
    is_context = True
    allow_children = []


class TitleContext(URLContext):
    tag_name = 'title'

