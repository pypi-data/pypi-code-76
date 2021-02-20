import base64


def b64_encode(s):
    return base64.b64encode(s.encode()).decode()


def b64_decode(s):
    return base64.b64decode(s).decode()
