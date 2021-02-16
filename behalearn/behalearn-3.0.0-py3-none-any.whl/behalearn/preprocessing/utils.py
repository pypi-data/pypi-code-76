def interpolate_custom_event(first_event, next_event, custom_event_timestamp):
    """Return interpolated coordinates of a custom event given the coordinates
    and timestamp of two consecutive events and the timestamp of the custom
    event.

    Parameters
    ----------
    first_event : tuple (coordinates..., timestamp)
        The first event with coordinates and a timestamp as the last element.
    
    next_event : tuple (coordinates..., timestamp)
        Event immediately following ``first_event`` containing  and a timestamp
        as the last element.
    
    custom_event_timestamp : float
        Timestamp of the custom event.

    Returns
    -------
    coords : tuple
        Coordinates of the interpolated custom event.

    Examples
    --------
    >>> interpolate_custom_event((1, 4, 5), (3, 6, 15), 10)
    (2, 5)
    >>> interpolate_custom_event((1, 4, 5, 5), (4, 7, 8, 20), 15)
    (3, 6, 7)

    Raises
    ------
    ValueError
        Value of ``custom_event_timestamp`` is below the timestamp of
        ``first_event`` or above the timestamp of ``next_event``.
    """
    first_coord, first_timestamp = first_event[:-1], first_event[-1]
    next_coord, next_timestamp = next_event[:-1], next_event[-1]

    if (custom_event_timestamp < first_timestamp
        or custom_event_timestamp > next_timestamp):
        raise ValueError(
            f'custom event timestamp {custom_event_timestamp}'
            f' is out of bounds ({first_timestamp}, {next_timestamp})')

    event_time_diff = next_timestamp - first_timestamp

    if event_time_diff != 0:
        ratio = (custom_event_timestamp - first_timestamp) / event_time_diff
    else:
        ratio = 0.5

    result = []
    for first_coord, next_coord in zip(first_coord, next_coord):
        result.append(first_coord + (next_coord - first_coord) * ratio)

    return tuple(result)


def trapezoid_diagonal_intersection(a, b, c, d):
    """Calculate coordinates of a point representing the intersection of the
    trapezoid diagonals.
    
    Trapezoid bases are represented by vertical lines connecting points ``ab``
    and ``cd``, respectively. Consequently, points ``a`` and ``b`` must have
    the same `x`-coordinate. The same restriction applies to points ``c`` and
    ``d``.
    
    The intersection may be used to determine, for example, the equal error
    rate (EER) from two points representing false match rate (FMR) and false
    non-match rate (FNMR) and their respective threshold values.
    
    Parameters
    ----------
    a : tuple of (float, float)
        Point A of a trapezoid.
    
    b : tuple of (float, float)
        Point B of a trapezoid.
    
    c : tuple of (float, float)
        Point C of a trapezoid.
    
    d : tuple of (float, float)
        Point D of a trapezoid.
    
    Returns
    -------
    intersection_coords : tuple of (float, float)
        Coordinates of the intersection of the trapezoid diagonals.
    
    Raises
    ------
    ValueError
        If point coordinates do not form a trapezoid (``a[0] != b[0]`` or
        ``c[0] != d[0]``).
    """
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    d_x, d_y = d

    if a_x != b_x or c_x != d_x:
        raise ValueError(
            f"point coordinates {a, b, c, d} do not form a trapezoid")

    # Switch coordinates around to make sure the computation is correct.

    if a_x < c_x:
        a_x, a_y, c_x, c_y = c_x, c_y, a_x, a_y
        b_x, b_y, d_x, d_y = d_x, d_y, b_x, b_y

    if a_y > b_y:
        a_x, a_y, b_x, b_y = b_x, b_y, a_x, a_y

    if c_y < d_y:
        c_x, c_y, d_x, d_y = d_x, d_y, c_x, c_y

    ab = abs(a_y - b_y)
    cd = abs(c_y - d_y)

    if cd != 0:
        ratio = ab / cd
    else:
        ratio = 1

    dx = abs(c_x - a_x) / (ratio + 1)
    dy = (c_y - a_y) / (ratio + 1)

    return c_x + dx, c_y - dy
