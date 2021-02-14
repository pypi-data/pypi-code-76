from lark import Lark, Transformer

from gozer_engine.base import BaseComponent

'''Does not support redtype/clones'''
gopher_dir_entry_grammar = r"""
    ?dom: ((text_block)(lastline))
    text_block: dom_entry*
    value: dict
        | list
        | string
        | newline
        | lastline
        | info_entity
        | plaintext_entity
        | dir_entity

    ?dom_entry   : info_entity
        | plaintext_entity
        | dir_entity
        | newline
        | lastline
    info_entity : "i"(user_name)*(tab)(selector)(tab)(host)(tab)(port)(newline)
    plaintext_entity   : "p"(data)(newline)
    dir_entity  : (gopher_type)(user_name)(tab)(selector)(tab)(host)(tab)(port)(newline)
    gopher_type : letter | digit
    tab         : /\\t/
    newline     : /\\n/
    lastline    : /\\n.\\n/
    user_name   : unascii
    data        : unascii
    selector    : unascii
    unascii     : (/(?!\\t)[ -~]/)*
    host        : unascii
    null        : "null" |"NULL"
    port        : digit_seq
    digit_seq   : digit*
    digit       : DIGIT
    letter      : LETTER

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value

    string : ESCAPED_STRING

    %import common.LETTER
    %import common.DIGIT
    %import common.NUMBER
    %import common._STRING_INNER
    %import common.ESCAPED_STRING
    %import common.WS
    %import common.NEWLINE
    %ignore WS
"""

class MyTransformer(Transformer):
    def digit(self, num: str) -> int:
        (num,) = num
        return int(num)
    def digit_seq(self, seq: list) -> str:
        seq_list = [str(x) for x in seq]
        return ''.join(seq_list)
    def unascii(self, items: list) -> str:
        return ''.join(items)
    def letter(self, item: list) -> str:
        (item,) = item
        return str(item)

class GopherSourceParser(BaseComponent):
    '''A Lark parser for processing Gopher
    page source code'''
    def __init__(self):
        self._grammar = gopher_dir_entry_grammar
        self._transformer = MyTransformer()
        self._root_node = 'dom'

    def _init_source_parser(self):
        '''Instantiate parser with the Gopher grammar'''
        self._parser = Lark(
            self._grammar,
            start=self._root_node
        )

    def parse_source(self, raw_response: str):
        '''Process network response into a Lark tree

        :param raw_response: raw response from the network module
        :type raw_response: str
        '''
        self._init_source_parser()
        
        # For lines that do not start with a gopher type
        # char, insert a `p` as the gopher type (plaintext)
        lines = raw_response.split('\n')
        lines_copy = []


        for line in lines:
            if len(line) == 0:
                continue

            if line[0] not in ['1', '7', '0', 'h', 'i']:
                copy = f'p{line}'
                lines_copy.append(copy)
            else:
                lines_copy.append(line)
            
        
        lines_copy.append('\n.\n')

        rejoined_response = '\n'.join(lines_copy)

        # TODO: Ugly workaround. Encoding + str casting may not be
        # necessary. Find out why Lark throws EOF errors
        # when string not encode (even when new line
        # is added): https://github.com/lark-parser/lark/issues/233
        source = str(rejoined_response.encode('ascii', errors='ignore'))
        source = source[1:]
        source = source.strip('\"')
        source = source.strip('\'')
        source = source.replace('\\\\', '\\')

        source_tree = self._parser.parse(source)
        transformed = MyTransformer().transform(source_tree)
        page_tree = transformed.children[0]

        self.mediator.notify(self, {
            'msg': 'source_parsed',
            'data': {
                'page_tree': page_tree
            }
        })