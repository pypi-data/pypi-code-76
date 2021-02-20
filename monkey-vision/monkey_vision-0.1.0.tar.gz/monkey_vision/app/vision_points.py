import concurrent.futures
from monkey_vision.app import vision_ui as vu, vision_text as vt

"""
--------------------------------------------------------------------------
CALCULATE THE POSSIBLE ACTION POINTS OF A PROVIDED IMAGE
Points are found from text elements or UI elements
--------------------------------------------------------------------------
"""


def get_vision_points(imageURI):
    """
    Multithreaded approach to get all the event points from a provided image
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_text = executor.submit(vt.get_paragraph_centers, imageURI)
        future_ui = executor.submit(vu.get_ui_centers, imageURI)
        paragraph_centers = future_text.result()
        ui_centers = future_ui.result()
        return paragraph_centers + ui_centers
