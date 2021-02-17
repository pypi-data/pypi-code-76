import re

__all__ = [
    "ANY_CHAR",
    "CARRIAGE_RETURN",
    "DIGIT",
    "END_OF_INPUT",
    "NEWLINE",
    "NON_DIGIT",
    "NON_WHITESPACE_CHAR",
    "NON_WORD",
    "NON_WORD_BOUNDARY",
    "NULL_BYTE",
    "ONE_OR_MORE",
    "ONE_OR_MORE_LAZY",
    "OPTIONAL",
    "START_OF_INPUT",
    "TAB",
    "WHITESPACE_CHAR",
    "WORD",
    "WORD_BOUNDARY",
    "ZERO_OR_MORE",
    "ZERO_OR_MORE_LAZY",
    "any_of",
    "any_of_chars",
    "anything_but_chars",
    "anything_but_range",
    "anything_but_string",
    "assert_ahead",
    "assert_behind",
    "assert_not_ahead",
    "assert_not_behind",
    "at_least",
    "back_reference",
    "between",
    "capture",
    "exactly",
    "from_regex",
    "group",
    "named_back_reference",
    "optional",
    "range",
    "re_flags_to_string",
    "to_regex",
]


def re_flags_to_string(flags):
    possible_flags = {
        re.ASCII: "a",
        re.IGNORECASE: "i",
        re.LOCALE: "L",
        re.UNICODE: "u",
        re.MULTILINE: "m",
        re.DOTALL: "s",
        re.VERBOSE: "x",
    }

    flagchrs = ""
    for flagval, flagchr in possible_flags.items():
        if flags & flagval:
            flagchrs += flagchr

    return f"(?{flagchrs})"


def to_regex(*args, flags=0, flags_in_re=False):
    pattern = "".join(args)

    if flags_in_re:
        flagstring = re_flags_to_string(flags)
        pattern = f"{flagstring}{pattern}"
        return pattern

    # TODO compile or check for validity or something
    return re.compile(pattern, flags=flags)


def from_regex(pattern):
    """it would be cool to be provide a "labeling" function which could generate
    the code from a given regex, as part of a debugging suite
    """
    pass


def optional(*args):
    return f'(?:{"".join(args)})?'


def capture(*args, name=None):
    name = f"?<{name}>" if name is not None else ""
    return f'({name}{"".join(args)})?'


def group(*args):
    return f'(?:{"".join(args)})'


def range(*args, negate=False):
    character_set = ""
    for arg in args:
        try:
            start, end = arg
            character_set += f"{start}-{end}"
        except:
            raise

    negate = "^" if negate else ""
    return f"[{negate}{character_set}]"


def anything_but_range(*args):
    return range(*args, negate=True)


def any_of_chars(*args):
    chars = "".join(args)
    return f"[{chars}]"


def anything_but_chars(*args):
    chars = "".join(args)
    return f"[^{chars}]"


def anything_but_string(string):
    return group("".join(f"[^{c}]" for c in string))


def exactly(length):
    return f"{{{length}}}"


def at_least(length):
    return f"{length},"


def between(minl, maxl):
    return f"{minl},{maxl}"


def any_of(*args):
    return group("|".join(args))


def back_reference(index):
    return f"\\{index}"


def named_back_reference(name):
    return f"\\k<{index}>"


def assert_ahead(*args):
    return f'(?={"".join(args)})'


def assert_not_ahead(*args):
    return f'(?!{"".join(args)})'


def assert_behind(*args):
    return f'(?<={"".join(args)})'


def assert_not_behind(*args):
    return f'(?<!{"".join(args)})'


ANY_CHAR = "."
WHITESPACE_CHAR = r"\s"
NON_WHITESPACE_CHAR = r"\S"
DIGIT = r"\d"
NON_DIGIT = r"\d"
WORD = r"\w"
NON_WORD = r"\W"
WORD_BOUNDARY = r"\b"
NON_WORD_BOUNDARY = r"\B"
NEWLINE = r"\n"
CARRIAGE_RETURN = r"\r"
TAB = r"\t"
NULL_BYTE = None
ONE_OR_MORE = r"+"
ONE_OR_MORE_LAZY = r"+?"
ZERO_OR_MORE = r"*"
ZERO_OR_MORE_LAZY = r"*?"
OPTIONAL = r"?"
START_OF_INPUT = r"^"
END_OF_INPUT = r"$"
