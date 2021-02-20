import math
from monkey_vision.app.math.utils import calc_center_of_shape


def areCoordinatesInRange(origin, target):
    """
    Method to check if a provided `target` coordinate is in range of of a origin coordinate.
    A coordinate is considered in range in case it has ONE pixel distance range in either axis, or both.
    This makes the coordinates be in the same line vertically or horizontally.
    :param origin:
    :param target:
    :return:
    """
    if origin is None or target is None:
        return False
    xRange = (origin[0] - 1, origin[0] + 1)
    yRange = (origin[1] - 1, origin[1] + 1)
    targetX = target[0]
    targetY = target[1]
    if xRange[0] <= targetX <= xRange[1] and yRange[0] <= targetY <= yRange[1]:
        return True
    return False


def isCoordinateInRectangle(point, rectangle, pixel_error_range=0):
    """
    Method to check if a provided coordinate is inside or in the border of a rectangle
    pixel_error_range is the range to be added on top of the rectangle properties
    within which the points is still considered as part of the array.
    Basically expanding the width and height of the rectangle.
    Needed for some text edges are outside of the predicted text area rectangle.
    :param point:
    :param rectangle:
    :param pixel_error_range:
    :return:
    """
    if point is not None or rectangle is not None:
        start = rectangle.get("start")
        end = rectangle.get("end")
        if start[0] - pixel_error_range <= point[0] <= (
            start[0] + (end[0] - start[0]) + pixel_error_range
        ) and start[1] - pixel_error_range <= point[1] <= (
            start[1] + (end[1] - start[1]) + pixel_error_range
        ):
            return True
    return False


def cleanTextEdges(edges, text_areas):
    """
    Method to clean all the edges/coordinates that belong to a text area.
    all text areas will be considered as a single entity
    :param edges:
    :param text_areas:
    :return:
    """
    # TODO improve looping and cleaning algorithm. e.g.  binary search tree
    cleanEdges = []
    if edges is not None and text_areas is not None:
        for coordinate in edges:
            isTextCoordinate = False
            for area in text_areas:
                if isCoordinateInRectangle(coordinate, area, 2):
                    isTextCoordinate = True
                    continue
            if not isTextCoordinate:
                cleanEdges.append(coordinate)
    return cleanEdges


def isHullInTextArea(convex_hull, text_area):
    """
    textArea is rectangle area
    convexHull si array of coordinates [ [[x1,y1]], [[x2,y2], ... ]]
    :param convex_hull:
    :param text_area:
    :return:
    """
    if convex_hull is not None and text_area is not None:
        for item in convex_hull:
            start = text_area["start"]
            end = text_area["end"]
            if start[0] <= item[0][0] <= end[0]:
                if start[1] <= item[0][1] <= end[1]:
                    return True
    return False


# TODO improve looping. e.g.  binary search tree
def cleanConvexHulls(convex_hulls, text_areas):
    """
    Method to clean all the convexHulls that have at least one coordinate under the text area rectangle.
    This method returns an array of convexHulls that do not have any coordinates under any of the areas.
    :param convex_hulls:
    :param text_areas:
    :return:
    """
    clean_convex_hulls = []
    if convex_hulls is not None and text_areas is not None:
        for hull in convex_hulls:
            is_hull_in_text_area = False
            for area in text_areas:
                is_hull_in_text_area = isHullInTextArea(hull, area)
                if is_hull_in_text_area:
                    break
            if not is_hull_in_text_area:
                clean_convex_hulls.append(hull)

    return clean_convex_hulls


def merge_common_elements_array(data):
    """
    Method to group provided array of elements that have possibly common elements amongst them.
    If arrays have at least one element in common they will be grouped together.
    :param data: Array. Example: [ [1, 2], [4,5,7], [1,33], ...]
    :return: Array of grouped sub arrays.
    """
    grouped_data = []
    for group in data:
        merge_index = -1
        for index in range(len(grouped_data)):
            if have_common_member(group, grouped_data[index]):
                merge_index = index
                break
        if merge_index >= 0:
            value = set(grouped_data[merge_index] + group)
            grouped_data[merge_index] = list(value)
        else:
            grouped_data.append(group)  # new group
    return grouped_data


def have_common_member(a, b):
    """
    Method to check if two arrays have any common elements amongst them.
    :param a: Array
    :param b: Array
    :return: Boolean
    """
    a_set = set(a)
    b_set = set(b)
    if a_set & b_set:
        return True
    else:
        return False


def find_center_of_convexHull(convexHull):
    """
    Calculate the center location from a provided array of coordinates of convexHulls
    :param convexHull: [ [[12, 12]], [[333,231]],...  ]
    :return:
    """
    totalX = 0
    totalY = 0
    length = len(convexHull)
    for hull in convexHull:
        item = hull[0]
        totalX += item[0]
        totalY += item[1]
    return int(round(totalX / length)), int(round(totalY / length))
