from jinja2 import Markup, escape
from lektor.pluginsystem import Plugin


def _nl2br(text):
    return Markup("<br>\n".join([escape(line) for line in text.splitlines()]))


class Nl2BrPlugin(Plugin):
    name = "lektor-nl2br"

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters["nl2br"] = _nl2br
