from __future__ import annotations
from gozer_engine.base import BaseComponent

class RenderEngine(BaseComponent):
    def __init__(self):
        self._type_map = {
            '1': '(DIR)',
            '7': '(?)',
            '0': '(FILE)',
            'h': '(HTML)',
            'i': '',
            'p': ''
        }

    def render_source(self, page_tree: Tree):
        '''Translate a Lark tree representation of a Gopher page
        into a DOM representation (list of dicts)

        :param page_tree: A Lark structured tree representing the Gopher page
        :type page_tree: lark.Tree
        '''
        dir_entry_fields = ['gopher_type', 'user_name', 'selector', 'host', 'port']
        info_entry_fields = ['user_name', 'selector', 'host', 'port']
        plaintext_entry_fields = ['data']


        dom = []

        # TODO: Consider refactor to not use chained
        # if-else
        line_count = 0
        for line in page_tree.children:

            gtype = [ x for x in line.find_data('gopher_type')]
            if line.data == 'info_entity':
                field_map = info_entry_fields
            elif line.data == 'dir_entity':
                field_map = dir_entry_fields
            elif line.data == 'plaintext_entity':
                field_map = plaintext_entry_fields
            elif line.data == 'newline' or line.data == 'lastline':
                field_map = []
            else:
                pass # Handle error

            line_map = {
                'data': {},
                'active': False,
                'position': line_count
            }

            for field in field_map:
                if len(field_map) == 0:
                    value = '\n'
                else:
                    value = [x for x in line.find_data(field)][0].children[0]

                line_map['data'][field] = value
            dom.append(line_map)
            line_count += 1  

        page_str = ''

        for entry in dom:
            # TODO: Find a better way to guarantee that gopher_type
            # is a string from within the grammar/parser
            if len(entry) == 0:  # I hate this
                line = '\n'
            else:
                # TODO: Update the parser to hard code
                # a gophertype of 'i' for any info_entity
                # token in order to remove the first branch
                # of this chain
                if entry['data'].get('gopher_type') is None:
                    entry['data']['gopher_type'] = 'i'

                label = self._type_map[str(entry['data']['gopher_type'])]
                padding = 7 - len(label) # Create a uniform left column
                line = f'{padding * " "}{label} {entry["data"].get("user_name")}\n'
            page_str += line
        
        self.mediator.notify(self, {
            'msg': 'page_rendered',
            'data': {
                'dom': dom,
                'page_str': page_str,
            }
        })