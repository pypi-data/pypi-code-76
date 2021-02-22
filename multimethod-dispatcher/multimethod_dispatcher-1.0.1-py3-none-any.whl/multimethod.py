"""
Dispatcher works for multimethods
this is the concept of having different implementations
for with the method name being the same.
"""


def multi(dispatch_fn):
    """Initialise function as a multimethod"""
    def _inner(*args, **kwargs):
        return _inner.__multi__.get(
            dispatch_fn(*args, **kwargs),
            _inner.__multi_default__
        )(*args, **kwargs)

    _inner.__multi__ = {}
    _inner.__multi_default__ = lambda *args, **kwargs: None  # Default default
    return _inner


def method(dispatch_fn, dispatch_key=None):
    """Register method as a part of multimethod"""
    def apply_decorator(func):
        if dispatch_key is None:
            # Default case
            dispatch_fn.__multi_default__ = func
        else:

            dispatch_fn.__multi__[dispatch_key] = func
        return dispatch_fn
    return apply_decorator
