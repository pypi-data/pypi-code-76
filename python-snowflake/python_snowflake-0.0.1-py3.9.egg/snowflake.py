from uuid import uuid4


def snowflake():
    return uuid4().hex[:6]
