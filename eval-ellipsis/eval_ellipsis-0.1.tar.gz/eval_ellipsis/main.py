"""Evaluate Ellipses using EvalEllipsis methods."""


class EvalEllipsis:
    """
    Calling any of the class functions causes the evaluating
    of all ellipses to the names of the associated
    variables, according to the selected case.
    """

    @classmethod
    def to_original_case(cls):
        cls._eval_ellipsis(str)

    @classmethod
    def to_screaming_snake_case(cls):
        cls._eval_ellipsis(cls._screaming_snake_case)

    @classmethod
    def to_snake_case(cls, local_vars: dict):
        cls._eval_ellipsis(local_vars, cls._snake_case)

    @classmethod
    def to_camel_case(cls, local_vars: dict):
        cls._eval_ellipsis(local_vars, cls._camel_case, True)

    @classmethod
    def to_lower_camel_case(cls, local_vars: dict):
        cls._eval_ellipsis(local_vars, cls._camel_case, False)

    @classmethod
    def to_lower_case(cls, local_vars: dict):
        cls._eval_ellipsis(local_vars, cls._lower_case)

    @staticmethod
    def _eval_ellipsis(local_vars: dict, case_func, *args):
        local_vars.update({key: case_func(key, *args) for key, value in local_vars.items() if value is ...})

    @classmethod
    def _screaming_snake_case(cls, text):
        """
        Transform text to SCREAMING_SNAKE_CASE

        :param text:
        :return:
        """
        if text.isupper():
            return text
        result = ''
        for pos, symbol in enumerate(text):
            if symbol.isupper() and pos > 0:
                result += '_' + symbol
            else:
                result += symbol.upper()
        return result

    @classmethod
    def _snake_case(cls, text):
        """
        Transform text to snake cale (Based on SCREAMING_SNAKE_CASE)

        :param text:
        :return:
        """
        if text.islower():
            return text
        return cls._screaming_snake_case(text).lower()

    @classmethod
    def _camel_case(cls, text, first_upper=False):
        """
        Transform text to camelCase or CamelCase

        :param text:
        :param first_upper: first symbol must be upper?
        :return:
        """
        result = ''
        need_upper = False
        for pos, symbol in enumerate(text):
            if symbol == '_' and pos > 0:
                need_upper = True
            else:
                if need_upper:
                    result += symbol.upper()
                else:
                    result += symbol.lower()
                need_upper = False
        if first_upper:
            result = result[0].upper() + result[1:]
        return result

    @classmethod
    def _lower_case(cls, text):
        return cls._snake_case(text).replace('_', ' ')
