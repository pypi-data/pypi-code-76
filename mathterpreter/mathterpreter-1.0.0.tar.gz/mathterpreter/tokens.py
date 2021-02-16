from dataclasses import dataclass
from typing import Optional


class TokenType:
    NUMBER = 0
    DECIMAL_PLACE = 1
    ADDITION_OPERATOR = 2
    SUBTRACTION_OPERATOR = 3
    MULTIPLICATION_OPERATOR = 4
    DIVISION_OPERATOR = 5
    SQRT_OPERATOR = 6
    POWER_OPERATOR = 7
    OPENING_BRACKET = 8
    CLOSING_BRACKET = 9


FORMATS = {

    TokenType.NUMBER: "{0.value}",
    TokenType.DECIMAL_PLACE: ".",
    TokenType.ADDITION_OPERATOR: "+",
    TokenType.SUBTRACTION_OPERATOR: "-",
    TokenType.MULTIPLICATION_OPERATOR: "*",
    TokenType.DIVISION_OPERATOR: "/",
    TokenType.SQRT_OPERATOR: "√",
    TokenType.POWER_OPERATOR: "^",
    TokenType.OPENING_BRACKET: "(",
    TokenType.CLOSING_BRACKET: ")"

}

@dataclass
class Token:
    type: TokenType
    value: Optional[float] = None

    def __str__(self):
        return FORMATS[self.type].format(self)
