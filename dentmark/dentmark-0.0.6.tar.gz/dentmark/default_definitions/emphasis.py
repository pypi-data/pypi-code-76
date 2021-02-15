from dentmark import TagDef

class Emphasis(TagDef):
    allow_children = [] # maybe b, i, a?

    def render_main(self):
        return f'<{self.tag_name}>{self.content}</{self.tag_name}>'

class Italic(Emphasis):
    tag_name = 'i'

    def render_main(self):
        return f'<i>{self.content}</i>'

class Bold(Emphasis):
    tag_name = 'b'

    def render_main(self):
        return f'<b>{self.content}</b>'

class StrikeThrough(Emphasis):
    tag_name = 's'

    def render_main(self):
        return f'<s>{self.content}</s>'

