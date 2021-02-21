import cv2
import numpy as np


# Get Canny edges for the provided asset image
def getImageEdges(imageUri):
    img = cv2.imread(imageUri)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(imgGray, 5, 100)
    return edges


# Method to get all the coordinates of the edges in the provided image.
# The coordinates include all the pixel coordinates of the WHITE points in the image.
def getEdgeCoordinates(edgesImage):
    if edgesImage is None:
        return []
    # used the `numpy.where()` method to retrieve a tuple indices of two arrays where the first array contains the
    # x-coordinates of the white points and the second array contains the y-coordinates of the white pixels.
    indices = np.where(edgesImage != [0])
    # used the `zip()` method to get a list of tuples containing the points.
    coordinates = zip(indices[1], indices[0])
    return list(coordinates)
