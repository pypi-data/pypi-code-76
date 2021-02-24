"""

"""


# Built-in

# Libs
import numpy as np

# Own modules

# Settings


def check_img_stats(img):
    """
    Check the stats of an image, print out its min and max values
    :param img:
    :return:
    """
    print(f'min: {np.min(img)}; max: {np.max(img)}')
