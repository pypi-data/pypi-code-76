from dentmark import TagDef


class List(TagDef):
    allow_children = ['li'] # maybe b, i, a?

    def render_main(self):
        return f'<{self.tag_name}>{self.content}</{self.tag_name}>'

class ListItem(TagDef):
    tag_name = 'li'
    exclude_children = []

    def render_main(self):
        return f'<li>{self.content}</li>'


class UnorderedList(List):
    tag_name = 'ul'

class OrderedList(List):
    tag_name = 'ol'
