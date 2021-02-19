"""Maps ticks helpers."""

from matplotlib.ticker import FuncFormatter


@FuncFormatter
def lat_ticks(lat, pos=None):  # pylint: disable=unused-argument
    """Latitude ticks formatter."""
    if lat == 90:
        return 'N.P.'

    if lat == 0:
        return 'Eq.'

    if lat == -90:
        return 'S.P.'

    if lat < 0:
        return f'{-lat}°S'

    return f'{lat}°N'


@FuncFormatter
def lon_e_ticks(lon_e, pos=None):  # pylint: disable=unused-argument
    """East longitude ticks formatter."""
    if lon_e % 180 == 0:
        return f'{lon_e % 360}°'

    return f'{lon_e % 360}°E'


@FuncFormatter
def lon_w_ticks(lon_w, pos=None):  # pylint: disable=unused-argument
    """West longitude ticks formatter."""
    if lon_w % 180 == 0:
        return f'{lon_w % 360}°'

    return f'{lon_w % 360}°W'
