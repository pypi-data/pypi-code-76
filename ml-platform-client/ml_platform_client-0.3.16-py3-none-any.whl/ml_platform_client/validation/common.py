def check_not_null(obj, message=None):
    if not message:
        message = 'unexpected null value'
    if obj is None:
            raise ValueError(message)
