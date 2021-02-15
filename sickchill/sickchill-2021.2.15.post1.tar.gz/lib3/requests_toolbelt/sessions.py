import requests

from ._compat import urljoin


class BaseUrlSession(requests.Session):
    """A Session with a URL that all requests will use as a base.

    Let's start by looking at an example:

    .. code-block:: python

        >>> from requests_toolbelt import sessions
        >>> s = sessions.BaseUrlSession(
        ...     base_url='https://example.com/resource/')
        >>> r = s.get('sub-resource/' params={'foo': 'bar'})
        >>> print(r.request.url)
        https://example.com/resource/sub-resource/?foo=bar

    Our call to the ``get`` method will make a request to the URL passed in
    when we created the Session and the partial resource name we provide.

    We implement this by overriding the ``request`` method so most uses of a
    Session are covered. (This, however, precludes the use of PreparedRequest
    objects).

    .. note::

        The base URL that you provide and the path you provide are **very**
        important.

    Let's look at another *similar* example

    .. code-block:: python

        >>> from requests_toolbelt import sessions
        >>> s = sessions.BaseUrlSession(
        ...     base_url='https://example.com/resource/')
        >>> r = s.get('/sub-resource/' params={'foo': 'bar'})
        >>> print(r.request.url)
        https://example.com/sub-resource/?foo=bar

    The key difference here is that we called ``get`` with ``/sub-resource/``,
    i.e., there was a leading ``/``. This changes how we create the URL
    because we rely on :mod:`urllib.parse.urljoin`.

    To override how we generate the URL, sub-class this method and override the
    ``create_url`` method.

    Based on implementation from
    https://github.com/kennethreitz/requests/issues/2554#issuecomment-109341010
    """

    base_url = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.create_url(url)
        return super(BaseUrlSession, self).request(
            method, url, *args, **kwargs
        )

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url)
