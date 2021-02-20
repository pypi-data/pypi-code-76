import math


def calc_distance(point1, point2):
    """
    Method to calculate the distance between two cardesian coordinates, (x, y).
    """
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
    )


def calc_center_of_shape(dataArray):
    """
    Calculate the center location from a provided array of coordinates of convexHulls
    :param dataArray: [ [12, 34], [233, 344], ... ] || [ (12, 34), (233, 344), ... ]
    :return:
    """
    totalX = 0
    totalY = 0
    length = len(dataArray)
    for item in dataArray:
        totalX += item[0]
        totalY += item[1]
    return int(round(totalX / length)), int(round(totalY / length))
