import json
from http import client
from urllib.parse import urlparse


URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}"
SVG_URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}.svg"


def _put(url, headers, body, redirects=5):
    parts = urlparse(url)
    ctr = client.HTTPSConnection if parts.scheme == 'https' else client.HTTPConnection
    connection = ctr(host=parts.hostname, port=parts.port)
    connection.request(
        'PUT', parts.path,
        body=body, headers=headers)
    response = connection.getresponse()
    if response.status in (301, 302, 307, 308):
        if redirects == 0:
            raise client.HTTPException("Too many redirects")
        _put(response.headers.get('location'), headers, body, redirects=redirects - 1)
    return response


def upload(server: str, user: str, repo: str, subject: str, status: str, color: str) -> None:
    url = URL_FORMAT.format(server=server, user=user, repo=repo, subject=subject)
    r = _put(url,
             headers={"Content-Type": "application/json"},
             body=json.dumps(dict(status=status, color=color)))
    if r.status >= 200 and r.status < 300:
        return SVG_URL_FORMAT.format(
            server=server, user=user, repo=repo, subject=subject)

    raise client.HTTPException("HTTP Error: {}".format(r.status))


def _mix_colors(c1, c2, v):
    """Mixes two colors according to v in the 0-1 range
    where 0 only r1 and 1 only r2 and e.g. 0.5 is exactly in between"""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return (int(r2 * v + r1 * (1 - v)),
            int(g2 * v + g1 * (1 - v)),
            int(b2 * v + b1 * (1 - v)))


def _format(color):
    """Formats an r, g, b tuple as a hex encoded string"""
    return '{:02x}{:02x}{:02x}'.format(*color)


def get_color(min_value: int, max_value: int, value: int) -> str:
    return to_color((value - min_value) / (max_value - min_value))


def to_color(v: float) -> str:
    """Converts a coverage percentage to a color"""
    gradient_stops = [
        (0.5, (0xe0, 0x5d, 0x44)),
        (0.9, (0x44, 0xcc, 0x11)),
    ]
    if v < gradient_stops[0][0]:
        return _format(gradient_stops[0][1])
    if v > gradient_stops[-1][0]:
        return _format(gradient_stops[1][1])

    a = (v - gradient_stops[0][0]) / (gradient_stops[1][0] - gradient_stops[0][0])
    return _format(_mix_colors(gradient_stops[0][1], gradient_stops[1][1], a))
