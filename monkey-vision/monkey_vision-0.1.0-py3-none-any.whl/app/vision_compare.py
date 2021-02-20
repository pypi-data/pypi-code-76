import cv2
from monkey_vision.app.vision import image_matching

"""
--------------------------------------------------------------------------
IMAGE PERCENTAGE COMPARE
--------------------------------------------------------------------------
"""


def get_percentage_match(filepath1, filepath2, showDebugWindow=False):
    if filepath1 == filepath2:
        return 100
    image1 = cv2.imread(filepath1)
    image2 = cv2.imread(filepath2)
    percentageMatch = image_matching.getMatchPercentage(
        image1, image2, isDebug=showDebugWindow
    )
    return percentageMatch


def get_percentage_match_file(image1, image2, showDebugWindow=False):
    percentageMatch = image_matching.getMatchPercentage(
        image1, image2, isDebug=showDebugWindow
    )
    return percentageMatch
