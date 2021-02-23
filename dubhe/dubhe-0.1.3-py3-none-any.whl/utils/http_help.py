def invoke_with_token(func, renew, **kwargs) -> (object, str):
    _, _, err = renew(False)
    if err is not None:
        return None, "renew token error"

    out, err_code, err_msg = func(**kwargs)
    if err_code == 497:  # token error
        _, _, err = renew(True)
        if err is not None:
            return None, "renew token error"

        out, err_code, err_msg = func(**kwargs)
    return out, err_msg


def invoke_with_retry(func, renew, **kwargs) -> (object, str):
    for i in range(3):
        out, err = invoke_with_token(func, renew, **kwargs)
        if err is None:
            return out, err
