class SignaldException(Exception):
    """
    Base class to translate signald's response payloads into python exceptions
    """

    def __init__(self, error_type, error_msg):
        self.type = error_type
        self.msg = error_msg

    def __str__(self):
        return f"{self.type}: {self.msg}"


def raise_error(response: dict):
    """
    Raise a python exception using a signald response payload
    """
    if response.get("type") == "profile_not_available":
        raise SignaldException("profile_not_available", response.get("data"))

    data = response.get("data", dict())
    if isinstance(data, list):
        error = response.get("error", False)
    else:
        error = response.get("error", data.get("error", False))
    if error:
        if isinstance(error, bool):
            type_ = response.get("type")
            msg = response["data"].get("message", "")
            req = response["data"].get("request", "")
            msg += f"{req}"
        elif isinstance(error, dict):
            type_ = error.get("type")
            msg = error.get("message", "")
            msg += "".join(error.get("validationResults", [""]))
        raise SignaldException(type_, msg)
