from dentmark import TagDef

class Table(TagDef):
    tag_name = 'table'
    allow_children = ['tr']

    def render_main(self):
        return f'<table border="1">{self.content}</table>'

class TableRow(TagDef):
    tag_name = 'tr'
    allow_children = ['td']

    def render_main(self):
        #TODO figure out how to exclude text nodes
        #filter_content = [_ for _ in self.content if _.is_element]
        return f'<tr>{self.content}</tr>'

class TableCell(TagDef):
    tag_name = 'td'

    #TODO probably should allow links and some other tags too
    allow_children = ['colspan', 'rowspan', 'align']


    def render_main(self):
        colspan = self.context.get('colspan')
        rowspan = self.context.get('rowspan')

        #TODO better validation to make sure this is one of the
        # allowed values: right, left, center, etc.
        align = self.context.get('align')

        attrs = ''
        for ctx in ('colspan', 'rowspan', 'align'):
            ctx_val = self.context.get(ctx)
            if ctx_val:
                attrs += f' {ctx}="{ctx_val}"'

        return f'<td{attrs}>{self.content}</td>'


class ColspanContext(TagDef):
    tag_name = 'colspan'
    is_context = True
    allow_children = []

class RowspanContext(TagDef):
    tag_name = 'rowspan'
    is_context = True
    allow_children = []

class AlignContext(TagDef):
    tag_name = 'align'
    is_context = True
    allow_children = []
