from dentmark import TagDef

class Headline(TagDef):
    allow_children = [] # maybe b, i, a?

    def render_main(self):
        return f'<{self.tag_name}>{self.content}</{self.tag_name}>'

class H1(Headline):
    tag_name = 'h1'

class H2(Headline):
    tag_name = 'h2'

class H3(Headline):
    tag_name = 'h3'

class H4(Headline):
    tag_name = 'h4'

class H5(Headline):
    tag_name = 'h5'

class H6(Headline):
    tag_name = 'h6'
