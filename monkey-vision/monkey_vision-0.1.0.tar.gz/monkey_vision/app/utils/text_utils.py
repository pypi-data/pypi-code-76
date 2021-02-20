import math
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from monkey_vision.app.math import data_sorting
from monkey_vision.app.utils import data_utils as dataUtils


def getTextAreas(image):
    """
    Method to detect all text areas in the provided image
    returns an array of all the rectangles enclosing these text areas
    :param image:
    :return:
    """
    if image is None:
        return []
    textAreas = []
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(d["text"])
    for i in range(n_boxes):
        if int(d["conf"][i]) > 60:
            (x, y, w, h) = (
                d["left"][i],
                d["top"][i],
                d["width"][i],
                d["height"][i],
            )
            rectangle = {"start": (x, y), "end": (x + w, y + h)}
            textAreas.append(rectangle)
    return textAreas


def groupTextParagraphs(text_areas):
    """
    Method to group text areas for each word into text areas for same paragraph
    Merging is done by checking the distance of each text area rectangles from all directions
    and merging then into a larger rectangle area.
    :param text_areas:
    :return:
    """
    sortedAreas = data_sorting.sortTextAreas(text_areas)
    maxLength = len(sortedAreas)
    groups = []

    # For each item of we test it against 3 items closest to current index
    # In case either of close range is achieved an encoded string is assigned to each of the group
    for i in range(maxLength):
        check_indexes = [i - 3, i - 2, i - 1, i + 1, i + 2, i + 3]
        in_range_indexes = []
        for index in check_indexes:
            if 0 <= index < maxLength:
                in_range_indexes.append(index)

        current_item = sortedAreas[i]
        for range_index in in_range_indexes:
            same_paragraph_indexes = []
            are_in_same_paragraph = areTextAreasInSameParagraph(
                current_item, sortedAreas[range_index]
            )
            if are_in_same_paragraph:
                same_paragraph_indexes.append(range_index)
            if len(same_paragraph_indexes) > 0:
                # some items found
                same_paragraph_indexes.append(i)
                groups.append(same_paragraph_indexes)

    paragraphs = []
    grouped_words = dataUtils.merge_common_elements_array(groups)

    for group in grouped_words:
        arr = []
        for word_index in group:
            word = sortedAreas[word_index]
            arr.append(word["start"])
            arr.append(word["end"])
        box = cv2.minAreaRect(np.asarray(arr))
        pts = cv2.boxPoints(box)  # 4 outer corners
        paragraphs.append(pts)
    return paragraphs


def areTextAreasInSameParagraph(area1, area2):
    """
    Method to check if the two provided text ares are close enough to be considered as they belong to the same paragraph
    Areas belong to the same text area in case the distance is a certain coefficient,
     less than the height of the text(line height).
    :param area1: rectangle area
    :param area2: rectangle area
    :return:
    """
    if area1 is not None and area2 is not None:
        distance = rect_distance(area1, area2)
        if distance < 20:
            return True
    return False


def rect_distance(rect1, rect2):
    """
    Method to calculate the distance between two text area rectangles
    :param rect1:
    :param rect2:
    :return:
    """
    x1 = rect1["start"][0]
    y1 = rect1["start"][1]
    x1b = rect1["end"][0]
    y1b = rect1["end"][1]
    x2 = rect2["start"][0]
    y2 = rect2["start"][1]
    x2b = rect2["end"][0]
    y2b = rect2["end"][1]

    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return distance((x1, y1b), (x2b, y2))
    elif left and bottom:
        return distance((x1, y1), (x2b, y2b))
    elif bottom and right:
        return distance((x1b, y1), (x2, y2b))
    elif right and top:
        return distance((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:  # rectangles intersect
        return 0.0


def distance(point1, point2):
    return math.sqrt(
        (
            math.pow((point2[0] - point1[0]), 2)
            + math.pow((point2[1] - point1[1]), 2)
        )
    )
