import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -----------------------------
# Get the X Y size of the image
def _get_image_size(array):

    # Get the corrected limits
    if len(array.shape) == 2:
        y_max, x_max = array.shape[0], array.shape[1]
    else:
        y_max, x_max = array.shape[1], array.shape[2]

    return y_max, x_max

# --------------
# Crop the array
def _crop_array(array, top_left, bottom_right):

    # Check that the new image is within the large image
    image_size = _get_image_size(array)
    for i in range(0,2):
        low_limit = top_left[i]
        high_limit = bottom_right[i]

        if low_limit < 0 or high_limit > image_size[i]:
            raise Exception("The image cannot be cropped using the given coordinates")

    # Get the corrected limits
    if len(array.shape) == 2:
        new_array = array[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
    else:
        new_array = array[:,top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]

    return new_array

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Crop the image using the given points
def crop(array, top_left=(0,0), bottom_right=None):

    # Get the bottom right limit
    if bottom_right is None:
        bottom_right = _get_image_size(array)[::-1]

    new_array = _crop_array(array, top_left[::-1], bottom_right[::-1])

    return new_array
