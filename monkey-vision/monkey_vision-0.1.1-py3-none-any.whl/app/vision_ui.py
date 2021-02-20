import cv2
from monkey_vision.app.vision_text import get_text_areas
from monkey_vision.app.vision import edges as edgeDetector
from monkey_vision.app.utils import data_utils as dataUtils
from monkey_vision.app.vision import contours_utils

"""
--------------------------------------------------------------------------
IMAGE PROCESSING UI ELEMENTS
--------------------------------------------------------------------------
"""


def get_ui_centers(imageURI):
    """
    Method returns the center points of UI elements in the provided image.
    UI element is considered everythin that is not a text element.
    """

    """
    UI element detection
    --------------------------------------------------------------------------
    """
    textAreas = get_text_areas(imageURI)

    edgesImage = edgeDetector.getImageEdges(imageURI)
    contours, hierarchy = cv2.findContours(
        edgesImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # contours_utils.drawConvexHull(contours, image)
    convexHulls = contours_utils.getConvexHulls(contours)

    # filter ConvexHulls that are under text areas
    cleanConvexHulls = dataUtils.cleanConvexHulls(convexHulls, textAreas)

    ui_centers = []

    # Extract centers of convex hulls
    for item in cleanConvexHulls:
        center = dataUtils.find_center_of_convexHull(item)
        ui_centers.append(center)

    return ui_centers


def get_clean_edges(imageURI):
    textAreas = get_text_areas(imageURI)

    edgesImage = edgeDetector.getImageEdges(imageURI)
    contours, hierarchy = cv2.findContours(
        edgesImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    coordinates = edgeDetector.getEdgeCoordinates(edgesImage)
    cleanEdges = dataUtils.cleanTextEdges(coordinates, textAreas)
    return cleanEdges


def get_convex_hull(imageURI):
    textAreas = get_text_areas(imageURI)
    edgesImage = edgeDetector.getImageEdges(imageURI)
    contours, hierarchy = cv2.findContours(
        edgesImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # contours_utils.drawConvexHull(contours, image)
    convexHulls = contours_utils.getConvexHulls(contours)
    # filter ConvexHulls that are under text areas
    cleanConvexHulls = dataUtils.cleanConvexHulls(convexHulls, textAreas)
    return cleanConvexHulls
