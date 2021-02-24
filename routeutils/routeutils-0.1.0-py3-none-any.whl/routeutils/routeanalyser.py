import numpy as np
from routeutils.Utils.utils import makeNewPoint
from routeutils.LineSegment.linesegment import LineSegment

def isPointInsideRoute(latitude: float, longitude: float, route: list, margin: float = 10) -> bool:
    """
    Calculates whether a point is within a route considering a margin between the point and the route.
    The coordinates must be in decimal format, ex: (-24.234123, -50.123321).

    The route must be a list of lists, in the GeoJson format, [longitude, latitude],
     ex: [[-24.234123, -50.123321], [-24.234123, -50.123321], [-24.234123, -50.123321]].

    :param latitude: latitude of the testing point.
    :param longitude: longitude of the testing point.
    :param route: the route being tested.
    :param margin: The margin, in meters, to be considered between the point and the route
     to decide if the point is within the route (usually related to GPS inaccuracy). Default value 10 meters.
    :return: true if the point is within the route considering the given margin, otherwise false.
    """

    pointOfInterest = (latitude, longitude)

    for pointIndex in range(len(route) - 1):
        routePointA = makeNewPoint(route[pointIndex])
        routePointB = makeNewPoint(route[pointIndex + 1])

        lineSegment = LineSegment(routePointA, routePointB)

        if lineSegment.isPointInLine(pointOfInterest, margin):
            return True
    return False