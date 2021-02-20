"""
This is a python port of super-expressive, a js library to make regular expressions easier to read and generate. 

"""
import re
from typing import Union, List


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


def re_flags_to_string(flags: int=0) -> str:
    """
    Turn a set of `re` flags into a string suitable for inclusion in a regex.

    >>> import superexpressive as se
    >>> se.re_flags_to_string(re.A)
    '(?a)'

    >>> import superexpressive as se
    >>> se.re_flags_to_string(re.IGNORECASE | re.LOCALE)
    '(?iL)'

    >>> import superexpressive as se
    >>> se.re_flags_to_string()
    ''

    """
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

    return f"(?{flagchrs})" if flagchrs else ""


def to_regex(*args:List[str], flags:int=0, compile:bool=True) -> Union[str, re.compile]:
    """ Turn a collection of strings into a regex. 

    If compile is True, return a re.compile object. If false, return a regex 
        string in the python style.

    >>> import superexpressive as se
    >>> se.to_regex(
    ...     se.START_OF_INPUT,
    ...     se.optional("0x"),
    ...     se.capture(se.range(("a", "f"), ("A", "F"), ("0", "9")), se.exactly(4)),
    ...     se.END_OF_INPUT,
    ...     compile=False
    ... )
    '^(?:0x)?([a-fA-F0-9]{4})$'

    >>> import superexpressive as se
    >>> se.to_regex(compile=False)
    ''

    # TODO: More tests, like flags

    """
    pattern = "".join(args)

    if compile:
        return re.compile(pattern, flags=flags)
    else:
        flagstring = re_flags_to_string(flags)
        pattern = f"{flagstring}{pattern}"
        return pattern


def from_regex(pattern:str) -> str:
    """it would be cool to be provide a "labeling" function which could generate
    the code from a given regex, as part of a debugging suite
    """
    raise NotImplementedError()


def optional(*args:List[str]) -> str:
    """A optional non-capturing group of the items inside.

    >>> import superexpressive as se
    >>> se.optional(se.DIGIT)
    '(?:\\\\d)?'

    """
    return f'(?:{"".join(args)})?'


def capture(*args:List[str], name:Union[str,None]=None) -> str:
    """A group that captures its contents.

    >>> import superexpressive as se
    >>> se.capture(se.range(("a", "f"), ("0", "9")), 'XXX')
    '([a-f0-9]XXX)'

    """
    name = f"?<{name}>" if name is not None else ""
    return f'({name}{"".join(args)})'


def group(*args:List[str]) -> str:
    """A group that does not capture its contents.

    >>> import superexpressive as se
    >>> se.group(se.range(("a", "f"), ("0", "9")), 'XXX')
    '(?:[a-f0-9]XXX)'

    """
    return f'(?:{"".join(args)})'


def range(*args:List[str], negate:bool=False) -> str:
    """An item that matches a range of characters by ascii code.

    >>> import superexpressive as se
    >>> se.range(('A', 'F'))
    '[A-F]'

    """
    character_set = ""
    for arg in args:
        try:
            start, end = arg
            character_set += f"{start}-{end}"
        except:
            raise

    negate = "^" if negate else ""
    return f"[{negate}{character_set}]"


def anything_but_range(*args:List[str]) -> str:
    """ An item that matches anything but a range of characters. 

    >>> import superexpressive as se
    >>> se.anything_but_range(('A', 'F'))
    '[^A-F]'

    """
    return range(*args, negate=True)


def any_of_chars(*args:List[str]) -> str:
    """ A length 1 item that matches any of the included characters.

    >>> import superexpressive as se
    >>> se.any_of_chars('A', 'F', 'dkja')
    '[AFdkja]'

    """
    # TODO uniq
    chars = "".join(args)
    return f"[{chars}]"


def anything_but_chars(*args:List[str]) -> str:
    """ A length 1 item that matches anything but the included characters.

    >>> import superexpressive as se
    >>> se.anything_but_chars('A', 'F', 'dkja')
    '[^AFdkja]'

    """
    # TODO uniq
    chars = "".join(args)
    return f"[^{chars}]"


def anything_but_string(string:str) -> str:
    """ Match anything except the provided string.

    >>> import superexpressive as se
    >>> se.anything_but_string('test')
    '(?:[^t][^e][^s][^t])'

    """
    return group("".join(f"[^{c}]" for c in string))


def exactly(length:int) -> str:
    """ Match the previous pattern exactly `length` times.

    >>> import superexpressive as se
    >>> se.exactly(4)
    '{4}'
    
    >>> import superexpressive as se
    >>> se.DIGIT + se.exactly(6)
    '\\\\d{6}'

    """
    return f"{{{length}}}"


def at_least(length:int) -> str:
    """ Match the previous pattern at least `length` times, greedily.

    >>> import superexpressive as se
    >>> se.at_least(4)
    '{4,}'
    
    >>> import superexpressive as se
    >>> se.DIGIT + se.at_least(6)
    '\\\\d{6,}'

    """
    return f"{{{length},}}"


def between(minl:int, maxl:int) -> str:
    """ Match the previous pattern at between `minl` and `maxl` times, greedily.

    >>> import superexpressive as se
    >>> se.between(4,8)
    '{4,8}'
    
    >>> import superexpressive as se
    >>> se.DIGIT + se.between(6,8)
    '\\\\d{6,8}'
    
    """
    return f"{{{minl},{maxl}}}"


def any_of(*args:List[str]) -> str:
    """ Match any of the given arguments.

    >>> import superexpressive as se
    >>> se.any_of('A', 'F', 'dkja')
    '(?:A|F|dkja)'

    # TODO: is a non-capturing group really neccesary here?
    """
    return group("|".join(args))


def back_reference(index:int) -> str:
    """ Refer to an earlier captured group by 1-based index.

    >>> import superexpressive as se
    >>> se.back_reference(2)
    '\\\\2'
    
    # TODO: actual example of using this

    """
    # TODO error handling 
    return f"\\{index}"


def named_back_reference(name:str) -> str:
    """ Refer to an earlier captured group by name.

    >>> import superexpressive as se
    >>> se.named_back_reference('test')
    '\\\\k<test>'
    
    # TODO: actual example of using this

    """
    # TODO error handling 
    return f"\\k<{name}>"


def assert_ahead(*args:List[str]) -> str:
    """ Check, but do not consume, that the regex matches the next part of the string.

    >>> import superexpressive as se
    >>> se.assert_ahead('test')
    '(?=test)'
    
    # TODO: actual example of using this

    """
    return f'(?={"".join(args)})'


def assert_not_ahead(*args:List[str]) -> str:
    """ Check, but do not consume, that the regex does not match the next part of the string.

    >>> import superexpressive as se
    >>> se.assert_not_ahead('test')
    '(?!test)'
    
    # TODO: actual example of using this

    """
    return f'(?!{"".join(args)})'


def assert_behind(*args:List[str]) -> str:
    """ Check, that the regex matches the previous part of the string.

    >>> import superexpressive as se
    >>> se.assert_behind('test')
    '(?<=test)'
    
    # TODO: actual example of using this

    """
    return f'(?<={"".join(args)})'


def assert_not_behind(*args:List[str]) -> str:
    """ Check, that the regex does not match the previous part of the string.

    >>> import superexpressive as se
    >>> se.assert_not_behind('test')
    '(?<!test)'
    
    # TODO: actual example of using this

    """
    return f'(?<!{"".join(args)})'


#: Matches any character except a newline.
ANY_CHAR = "."
#: Matches any whitespace character
WHITESPACE_CHAR = r"\s"
#: Matches any non-whitespace character, this is the inverse of WHITESPACE_CHAR
NON_WHITESPACE_CHAR = r"\S"
#: Matches any digit character, is the equivalent of range 0-9
DIGIT = r"\d"
#: Matches any non-digit character, this is the inverse of DIGIT
NON_DIGIT = r"\d"
#: Matches any alphanumeric character a-z, A-Z, 0-9, or underscore
#: in bytes patterns or string patterns with the ASCII flag.
#: In string patterns without the ASCII flag, it will match the
#: range of Unicode alphanumeric characters (letters plus digits
#: plus underscore). 
WORD = r"\w"
#: Matches the complement of WORD
NON_WORD = r"\W"
#: Matches the empty string, but only at the start or end of a word.
WORD_BOUNDARY = r"\b"
#: Matches the empty string, but not at the start or end of a word.
NON_WORD_BOUNDARY = r"\B"
#: Matches a newline character.
NEWLINE = r"\n"
#: Matches a carriage return.
CARRIAGE_RETURN = r"\r"
#: Matches a tab character.
TAB = r"\t"
#: Matches 1 or more (greedy) repetitions of the preceding expression
ONE_OR_MORE = r"+"
#: Non-greedy match for one or more repetitions of the previous expression
ONE_OR_MORE_LAZY = r"+?"
#: Matches 0 or more (greedy) repetitions of the preceding RE.
#: Greedy means that it will match as many repetitions as possible.
ZERO_OR_MORE = r"*"
#: Non-greedy version of the zero or more match
ZERO_OR_MORE_LAZY = r"*?"
#: Matches 0 or 1 (greedy) of the preceding RE.
OPTIONAL = r"?"
#: Matches the start of the string.
START_OF_INPUT = r"^"
#: Matches the end of the string or just before the newline at the end of the string.
END_OF_INPUT = r"$"
