import click


class UrlParamType(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        """ Parses the url input """
        url_prefixes = ["http://", "https://", "localhost"]

        try:
            if not any([value.startswith(url_prefix) for url_prefix in url_prefixes]):
                raise ValueError
            return value
        except ValueError:
            self.fail(f"{value!r} is not a valid url", param, ctx)


# Add type for param/header

URL = UrlParamType()
