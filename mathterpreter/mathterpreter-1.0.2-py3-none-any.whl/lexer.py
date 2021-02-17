from mathterpreter.tokens import Token, TokenType
from mathterpreter.exceptions import MathSyntaxError
from typing import List

class Lexer:

    def __init__(self, string: str = ""):
        self.string = string
        self.__string = iter(string)
        self.tokens: List[Token] = []
        self.__character = None
        self.__iterate_string__()

    def __iterate_string__(self):
        try:
            self.__character = next(self.__string)
        except StopIteration:
            self.__character = None

    def generate_tokens(self):
        while self.__character is not None:
            if self.__character in (" ", "\t", "\n"):
                self.__iterate_string__()
                continue
            elif self.__character == "+":
                yield Token(TokenType.ADDITION_OPERATOR)
            elif self.__character == "-":
                yield Token(TokenType.SUBTRACTION_OPERATOR)
            elif self.__character == "*":
                yield Token(TokenType.MULTIPLICATION_OPERATOR)
            elif self.__character == "/":
                yield Token(TokenType.DIVISION_OPERATOR)
            elif self.__character in ("**", "^"):
                yield Token(TokenType.POWER_OPERATOR)
            elif self.__character in ("sqrt", "√"):
                yield Token(TokenType.SQRT_OPERATOR)
            elif self.__character == "(":
                yield Token(TokenType.OPENING_BRACKET)
            elif self.__character == ")":
                yield Token(TokenType.CLOSING_BRACKET)
            if self.__character in ("-", "+", "*", "/", "**", "^", "sqrt", "√", "(", ")"):
                self.__iterate_string__()
            elif self.__character == "." or self.__character.isdigit():
                yield self.__get_number__()
            else:
                raise MathSyntaxError("Unsupported token", f"{self.string}\n{'^'.rjust(self.string.index(self.__character) + 1)}")

    def tokenize(self):
        for token in self.generate_tokens():
            self.tokens.append(token)
        return self.tokens

    def __get_number__(self):
        decimal = 0
        string = self.__character
        self.__iterate_string__()
        while self.__character is not None and (self.__character.isdigit() or self.__character == ".") and decimal < 2:
            if self.__character == ".":
                decimal += 1

            string += self.__character
            self.__iterate_string__()

        if string.startswith('.'):
            string = '0' + string
        if string.endswith('.'):
            string += '0'

        return Token(TokenType.NUMBER, float(string))

    def __str__(self):
        return "\n".join([z.__str__() for z in self.tokens])
