from lark import Tree, Lark
from .margo_transformer import MargoTransformer
from ..exceptions import MargoParseException
import os


def grammar():
    grammar_file_path = os.path.join(os.path.split(__file__)[0], "margo.lark")
    grammar_content = open(grammar_file_path).read()
    return Lark(grammar_content, start="block", regex=True)


def get_tree(source: str):
    return grammar().parse(source)


def transform(tree):
    return MargoTransformer().transform(tree)


def tokenize(source: str):
    try:
        return transform(get_tree(source))
    except Exception as e:
        raise MargoParseException(e)
