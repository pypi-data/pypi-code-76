"""
    Therefore, everything not in jerome.k.PRINTABLE must not be in normal use within a text.
    The idea of de-glossing a string is to replace all these "illegal characters"
        with a single character reserved for this purpose.
    This process is reversible given a "gloss file" of format:
    List[str] = ["replacement character", "first replaced character", "second", "etc."]
"""

import re
import typing as t  # noqa: E902
import string


def degloss(text: str, mark: str, allowed: t.Union[str] = None) -> t.Tuple[str, str]:
    """Replaces all "illegal" characters (i) in text.
    Here, illegal means not in Jerome.k.PRINTABLE
    Returns (processed text, gloss_file).
    gloss_file format is:
        gloss_mark, i1, i2, etc...
    """
    notin = re.compile(f"[^{allowed if allowed is not None else string.printable}]")
    gloss_list = [mark]

    def gloss_repl(matchobj):
        gloss_list.append(matchobj.group(0))
        return gloss_list[0]

    processed = re.sub(notin, repl=gloss_repl, string=text)
    return (processed, "".join(gloss_list))


def gloss(s: str, gloss_file: str) -> str:
    """Restores characters in s from gloss_file."""
    gloss_list = list(gloss_file)
    g = gloss_list.pop(0)

    def degloss_repl(matchobj):
        return gloss_list.pop(0)

    o = re.sub(g, repl=degloss_repl, string=s)
    return o
