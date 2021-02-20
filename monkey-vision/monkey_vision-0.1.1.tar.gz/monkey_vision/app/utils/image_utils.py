import cv2


def imcrop(imagePath, center):
    """
    Method to crop the an image specified in the imagePath around the center specified in the function arguments.
    """
    (x, y) = (int(x) for x in center[1:-1].split(","))
    area = 100  # width and height in pixels around the center.
    image = cv2.imread(imagePath)
    height, width, channels = image.shape

    start_y = (y - area) if ((y - area) >= 0) else 0
    start_x = (x - area) if ((x - area) >= 0) else 0
    end_y = (y + area) if (((y + area)) < height) else (height - 1)
    end_x = (x + area) if (((x + area)) < width) else (width - 1)

    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image
