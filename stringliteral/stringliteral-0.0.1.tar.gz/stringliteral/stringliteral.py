"""Stringliteral"""


class StringLiteral:
    """Stringliteral class.

    Inherit your own string literal class from this one.
    """

    @classmethod
    def contains(cls, value: str) -> bool:
        """Evaluate whether the value belongs to the defined stringliteral."""
        evaluated_vals = []
        for val in dir(cls):
            if str.isupper(val):
                _val = getattr(cls, val)
                evaluated_vals.append(_val)

        return value in evaluated_vals
