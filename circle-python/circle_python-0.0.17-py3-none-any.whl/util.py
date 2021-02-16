import circle
from circle.circle_response import CircleResponse


def get_object_classes():
    from circle.object_classes import OBJECT_CLASSES

    return OBJECT_CLASSES


def convert_to_circle_object(response, api_key=None, klass_name=None):

    # If a CircleResponse is passed, return the StripeObject associated with it.

    if isinstance(response, CircleResponse):
        circle_response = response
        response = circle_response.data
    if isinstance(response, list):
        return [convert_to_circle_object(r, api_key) for r in response]
    elif get_object_classes().get(klass_name) is not None:
        return get_object_classes().get(klass_name).construct_from(response, api_key)
    elif isinstance(response, dict) and not isinstance(
        response, circle.circle_object.CircleObject
    ):

        return circle.circle_object.CircleObject.construct_from(response, api_key)
    elif isinstance(response, dict):
        return circle.circle_object.CircleObject.construct_from(response, api_key)
    else:
        return response
