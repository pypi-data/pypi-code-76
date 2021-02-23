import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename


def render(raw, ext=None, **kwargs):
    try:
        lexer = get_lexer_for_filename(ext)
    except pygments.util.ClassNotFound:
        lexer = get_lexer_by_name('python')
    formatters = HtmlFormatter(full=True, linenos=True, h1_lines=[1, 2])
    return highlight(raw, lexer, formatters)
