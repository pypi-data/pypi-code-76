import operator
import numpy as np

def count_list_items(item_list: list) -> list:
    possibilities = {}
    for item in item_list:
        if item not in possibilities:
            possibilities[item] = 1
        else:
            possibilities[item] = possibilities[item] + 1
    
    ordered_list = sorted(possibilities.items(), key=operator.itemgetter(1), reverse=True)
    return ordered_list

def count_pixels(img: np.ndarray) -> dict:
    pixel_dict = {}

    for row in img.tolist():
        for pixel in row:
            if len(pixel_dict) == 0 or str(pixel) not in pixel_dict:
                pixel_dict[str(pixel)] = 1
            else:
                pixel_dict[str(pixel)] = pixel_dict[str(pixel)] + 1
    return pixel_dict