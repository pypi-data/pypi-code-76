"tmp"

from lark import Lark
from lark.reconstruct import Reconstructor

# from .python_parser import python_parser3

g = """
start: a
?a: b "+"
?b: a | "+"
"""

p = Lark(g, parser='lalr', maybe_placeholders=False)

# test_python = '''
# print("Hello")
# '''

def test(parser, value):

    tree = parser.parse(value)

    new_code = Reconstructor(parser).reconstruct(tree)
    print (new_code)


s = "++"
print(p.parse(s))
test(p, s)

