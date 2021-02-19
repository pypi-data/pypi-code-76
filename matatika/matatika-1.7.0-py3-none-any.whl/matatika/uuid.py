"""UUID utilities"""

import re

VALID_UUID4_PATTERN = r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$'


def is_uuid4(value: str) -> bool:
    """Checks a given string is a valid version 4 UUID"""

    valid_uuid4 = re.compile(VALID_UUID4_PATTERN, re.IGNORECASE)

    if valid_uuid4.fullmatch(value):
        return True
    return False
