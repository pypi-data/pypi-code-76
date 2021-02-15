from dentmark import TagDef

class Annotation(TagDef):
    tag_name = 'a8n'
    allow_children = ['fn']

    def render_main(self):
        nth_of_type = self.nth_of_type + 1
        sup_id = f'fnref:{nth_of_type}'
        href = f'#fn:{nth_of_type}'

        return f'<span class="dm__a8n">{self.content}</span><sup id="{sup_id}"><a href="{href}" class="footnote-ref" role="doc-noteref">[{nth_of_type}]</a></sup>'


class FootNote(TagDef):
    tag_name = 'fn'
    add_to_collector = True
    allow_children = ['a', 'i']

    def render_main(self):
        return '' # don't render anything in-place

    def render_secondary(self):
        nth_of_type = self.nth_of_type + 1
        fn_id = f'fn:{nth_of_type}'
        href = f'#fnref:{nth_of_type}'
        return f'<li id="{fn_id}" role="doc-endnote"><p><a href="{href}" class="footnote-backref" role="doc-backlink">↩︎</a> {self.content}</p></li>'
