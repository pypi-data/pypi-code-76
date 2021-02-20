from .base_expression import BaseExpression

class ArithmeticExpression(BaseExpression):
    """An expression class for arithmetic operations.

    This is just a convenience class to logically separate its use from
    `EqualityExpressions`. This class is only used in `Number` datatypes and currently
    only in ``Number.add`` and ``Number.subtract``
    """
    pass
