"Demo of reconstructing Python (not working yet)"

from lark import Lark
from lark.reconstruct import Reconstructor

# g = """
# start: z
# ?z: a ("-" a)*
# ?a: b "+"
# ?b: a | "+"
# """

g = """
start: a
?a: b "+"
?b: a | "+"
"""


def test(parser, value):

    tree = parser.parse(value)

    new_code = Reconstructor(parser, {'_NEWLINE': lambda x: '\n'}).reconstruct(tree)
    print (new_code)


# p = Lark(g, parser='lalr', maybe_placeholders=False)
# s = "++++++++"
# print(p.parse(s))
# test(p, s)



from advanced.python_parser import python_parser3
test_python = '''
print("Hello")
'''
test(python_parser3, test_python)