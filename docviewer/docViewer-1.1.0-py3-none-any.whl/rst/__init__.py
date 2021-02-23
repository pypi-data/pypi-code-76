import os

from docutils import core
from docutils.parsers.rst.directives import register_directive

from .directives import Uml, Graph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STYLESHEET = os.path.join(BASE_DIR, 'default.css')

register_directive('uml', Uml)
register_directive('graph', Graph)


def render(*args, only_body=False, **kwargs):
    kwargs.setdefault('writer_name', 'html5')
    kwargs.setdefault('settings_overrides', {})
    if only_body:
        template = os.path.join(BASE_DIR, 'template_body.txt')
        kwargs['settings_overrides']['template'] = template
    # kwargs['settings_overrides'].setdefault('stylesheet_path',
    #                                         DEFAULT_STYLESHEET)
    return core.publish_string(*args, **kwargs)
