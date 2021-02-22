import urllib.parse

from jinja2 import Markup, escape
from lektor.pluginsystem import Plugin

_iframe_template = """<iframe{width}{height} src="https://www.youtube.com/embed/{id}"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  frameborder="0" allowfullscreen {attrs}></iframe>
"""


def _get_youtube_id(url):
    parsed_url = urllib.parse.urlparse(url)
    if "youtube.com" in parsed_url.netloc and parsed_url.path.strip("/"):
        if "/watch" in parsed_url.path:
            qs = urllib.parse.parse_qs(parsed_url.query)
            if "v" in qs:
                return qs["v"][0]
            return None
        elif "/embed" in parsed_url.path:
            return parsed_url.path.split("/embed")[1].strip("/")
        else:
            return None
    elif "youtu.be" in parsed_url.netloc and parsed_url.path.strip("/"):
        return parsed_url.path.strip("/")
    return None


def _youtube(url, width=None, height=None, attrs=None):
    id_ = _get_youtube_id(url)
    if not id_:
        return url
    width_str = ' width="{}"'.format(escape(width)) if width else ""
    height_str = ' height="{}"'.format(escape(height)) if height else ""
    attrs_str = (
        " ".join(
            ['{k}="{v}"'.format(k=escape(k), v=escape(v)) for k, v in attrs.items()]
        )
        if attrs
        else ""
    )
    return Markup(
        _iframe_template.format(
            width=width_str,
            height=height_str,
            id=escape(id_),
            attrs=attrs_str,
        )
    )


class YoutubeEmbedPlugin(Plugin):
    name = "lektor-youtube-embed"

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters["youtube"] = _youtube
