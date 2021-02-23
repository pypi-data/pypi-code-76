from typing import Any


def is_typing(cls: Any) -> bool:
    """
        Checks if this type is from typing module
        (because there is no base class to check with isinstance(...))

        >>> import typing
        >>> is_typing(typing.Optional[str])
        True
        >>> is_typing(str)
        False

    :param cls: Any Type
    :return: True if this type is typing and False if not
    """
    return cls.__module__ == "typing"


def cast_cap_words_to_lower(string: str) -> str:
    """
        Cast cap word format to lower case with underscores

        >>> cast_cap_words_to_lower("ClassName")
        'class_name'
        >>> cast_cap_words_to_lower("AnotherOne")
        'another_one'

    :param string: any str
    :return: str in lower case with underscores
    """
    if len(string) < 1:
        return string

    lower_str = string[0].lower()
    for ch in string[1:]:
        if ch.isupper():
            lower_str += "_"
        lower_str += ch.lower()

    return lower_str


def deep_merge_dicts(lhs: dict, rhs: dict) -> dict:
    """
    Deep merging two dicts
    """
    for key, value in rhs.items():
        if isinstance(value, dict):
            node = lhs.setdefault(key, {})
            deep_merge_dicts(node, value)
        else:
            lhs[key] = value

    return lhs
