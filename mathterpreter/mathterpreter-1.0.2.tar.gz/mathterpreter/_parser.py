from mathterpreter.nodes import *
from mathterpreter.tokens import TokenType, Token
from mathterpreter.exceptions import MathSyntaxError
from typing import List

class Parser:
    def __init__(self, tokens: List[Token]):
        self.__tokens = iter(tokens)
        self.token_list = tokens
        self.__token = None
        self.__index = -1
        self.__iterate_token__()

    def __iterate_token__(self):
        try:
            self.__token = next(self.__tokens)
            self.__index += 1
        except StopIteration:
            self.__token = None

    def parse(self):
        if self.__token is None:
            return None

        result = self.__addition_subtraction_base__()

        return result

    def __addition_subtraction_base__(self):
        if self.__token is None:
            output = ''.join([z.__str__() for z in self.token_list])
            raise MathSyntaxError("Expression expected", f"{output}\n{'^^^'.rjust(len(output) + 3)}")
        result = self.__multiplication_division__()
        while self.__token is not None:
            if self.__token.type == TokenType.ADDITION_OPERATOR:
                self.__iterate_token__()
                result = AdditionNode(result, self.__multiplication_division__())
            elif self.__token.type == TokenType.SUBTRACTION_OPERATOR:
                self.__iterate_token__()
                result = SubtractionNode(result, self.__multiplication_division__())
            else:
                break

        return result

    def __multiplication_division__(self):
        result = self.__exponentiation_root__()

        while self.__token is not None:
            if self.__token.type == TokenType.MULTIPLICATION_OPERATOR:
                self.__iterate_token__()
                result = MultiplicationNode(result, self.__exponentiation_root__())
            elif self.__token.type == TokenType.DIVISION_OPERATOR:
                self.__iterate_token__()
                result = DivisionNode(result, self.__exponentiation_root__())
            elif self.__token.type == TokenType.OPENING_BRACKET:
                result = MultiplicationNode(result, self.__literal_polarity__())
            else:
                break

        return result

    def __exponentiation_root__(self):
        result = self.__literal_polarity__()
        while self.__token is not None:
            if self.__token.type == TokenType.POWER_OPERATOR:
                self.__iterate_token__()
                result = ExponentiationNode(result, self.__literal_polarity__())
            elif self.__token.type == TokenType.SQRT_OPERATOR:
                self.__iterate_token__()
                result = RootNode(result, self.__literal_polarity__())
            else:
                break
        return result

    def __literal_polarity__(self):
        token = self.__token
        if token.type == TokenType.OPENING_BRACKET:
            self.__iterate_token__()
            result = self.__addition_subtraction_base__()
            self.__iterate_token__()
            return result

        else:
            self.__iterate_token__()
            if token.type == TokenType.NUMBER:
                return NumberNode(token.value)

            elif token.type == TokenType.ADDITION_OPERATOR:
                return PositiveNode(self.__literal_polarity__())

            elif token.type == TokenType.SUBTRACTION_OPERATOR:
                return NegativeNode(self.__literal_polarity__())
            else:
                output = [z.__str__() for z in self.token_list]
                raise MathSyntaxError("Unexpected token",
                                      f"{''.join(output)}\n{'^'.rjust(sum([len(z) for z in output[:self.__index]]))}")
