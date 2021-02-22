from typing import Union
from environs import Env
from canvasapi import Canvas
import base64
import hashlib

env = Env()
env.read_env()


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29
    :return: bytes representation of the CSCI salt
    """

    return bytes.fromhex(env("CSCI_SALT"))
    # Hint: use os.environment and bytes.fromhex


def get_csci_pepper() -> bytes:
    """Returns the appropriate pepper for CSCI E-29

    This is similar to the salt, but defined as the UUID of the Canvas course,
    available from the Canvas API.

    This value should never be recorded or printed.

    :return: bytes representation of the pepper
    """
    # get canvas value for uuid
    masquerade = {}
    canvas = Canvas(env("CANVAS_URL"), env("CANVAS_TOKEN"))
    course = canvas.get_course(env("CANVAS_COURSE_ID"), **masquerade)
    return base64.b64decode(str(course.uuid))
    # Hint: Use base64.b64decode to decode a UUID string to bytes


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest
    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """

    # check if input value is str
    if type(some_val) is str:
        some_val = some_val.encode()

    # check if input salt is str
    if type(salt) is str:
        salt = salt.encode()

    # raise error if both values are not either str or bytes
    if type(some_val) is not bytes and type(salt) is not bytes:
        raise TypeError("Incorrect file type for both inputs")

    # raise error if input value is not string or bytes
    if type(some_val) is not bytes:
        raise TypeError("Incorrect file type for input value")

    # creating hash value for salt and value
    if type(some_val) is bytes and type(salt) is bytes:
        return hashlib.sha256(salt+some_val).digest()

    # raise error if salt is of incorrect data type
    else:
        raise TypeError("Incorrect file type for salt")


def get_user_id(username: str) -> str:
    salt = get_csci_salt() + get_csci_pepper()
    return hash_str(username.lower(), salt=salt).hex()[:8]
