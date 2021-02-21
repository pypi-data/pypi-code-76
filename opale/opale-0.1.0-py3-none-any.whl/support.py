from pygments.style import Style
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Number,
    Operator,
    Generic,
    Whitespace,
    Punctuation,
    Other,
    Literal,
)


# Originally based on FlaskyStyle which was based on 'tango'.
class Opale(Style):
    background_color = "#f8f8f8"  # doesn't seem to override CSS 'pre' styling?
    default_style = ""

    styles = {}
