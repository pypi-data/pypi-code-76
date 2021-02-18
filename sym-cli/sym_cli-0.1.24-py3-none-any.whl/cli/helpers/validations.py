from .params import get_profile


def validate_resource(resource: str):
    try:
        get_profile(resource)
        return True
    except KeyError:
        return False
