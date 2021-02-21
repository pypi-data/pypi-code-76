import cv2
from monkey_vision.app.utils import text_utils
from monkey_vision.app.math import utils as math_utils

"""
--------------------------------------------------------------------------
IMAGE PROCESSING FOR TEXT CONTENT
--------------------------------------------------------------------------
"""


def get_paragraph_centers(imageURI):
    """
    Method returns the center points of text paragraph in the provided image.
    """
    image = cv2.imread(imageURI)
    paragraph_centers = []
    """
    Text detection paragraphs
    --------------------------------------------------------------------------
    """
    # get all text areas from the target image
    textAreas = text_utils.getTextAreas(image)
    paragraphs = text_utils.groupTextParagraphs(textAreas)

    for item in paragraphs:
        center = math_utils.calc_center_of_shape(item)
        paragraph_centers.append(center)

    return paragraph_centers


def get_text_areas(imageURI):
    """
    Method returns the text area rectangles found in the provided image.
    """
    image = cv2.imread(imageURI)
    textAreas = text_utils.getTextAreas(image)
    return textAreas


def get_paragraphs(imageURI):
    textAreas = get_text_areas(imageURI)
    paragraphs = text_utils.groupTextParagraphs(textAreas)
    return paragraphs
