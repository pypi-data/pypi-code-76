import cv2
import numpy as np


def drawConvexHull(contours, image):
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        cv2.drawContours(image, [hull], -1, (255, 0, 0), 2)


def getConvexHulls(contours):
    hulls = []
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        hulls.append(hull)
    return hulls


def drawMinRect(contours, image):
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
