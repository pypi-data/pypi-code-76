from tamarin.lamagram.config import ALLOWED_STATUS, ALLOWED_ALL
from tamarin import status


def validate_status(status_code):
    if ALLOWED_ALL:
        return True
    allowed_condition = [getattr(status, F'is_{method}', None) for method in ALLOWED_STATUS]
    for condition in allowed_condition:
        if condition and condition(status_code):
            return True
    if status_code in ALLOWED_STATUS:
        return True
    return False
