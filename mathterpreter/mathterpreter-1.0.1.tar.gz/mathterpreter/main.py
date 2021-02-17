from mathterpreter.lexer import Lexer
from mathterpreter._parser import Parser


def interpret(string: str):
    return Parser(Lexer(string).tokenize()).parse().evaluate()
