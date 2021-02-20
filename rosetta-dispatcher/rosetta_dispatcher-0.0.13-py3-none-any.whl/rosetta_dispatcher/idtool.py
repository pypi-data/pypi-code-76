import uuid


def get_timestamp(struuid: str):
    return (uuid.UUID(struuid).time - 0x01b21dd213814000) / 1e7


def gen_uuid():
    return str(uuid.uuid1())
