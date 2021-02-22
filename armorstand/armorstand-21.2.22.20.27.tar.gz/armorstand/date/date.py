from datetime import datetime
from enum import Enum
from typing import List


class DateCode(Enum):
    SHORT_DAY_NAME = "%a"
    DAY_NAME = "%A"
    DAY = "%-d"
    ZERO_PADDED_DAY = "%-d"
    SHORT_MONTH = "%b"
    MONTH = "%B"
    MONTH_NUMBER = "%-m"
    YEAR = "%Y"
    SHORT_YEAR = "%y"
    COMMA = ","
    SLASH = "/"


def get_date(order: List[DateCode], return_strf=False) -> str:
    """Get the date using codes from DateCode, or a strftime builder

    Parameters:
        order (List[DateCode]): the date format
        return_strf (bool, default False): use to return the datetime `strftime` format.

    Use return_strf for testing.
    """

    now = datetime.now()

    string = ""
    for index, code in enumerate(order):
        try:
            next_code = order[index + 1]
        except:
            next_code = None

        string += code.value

        if next_code not in (DateCode.COMMA, DateCode.SLASH) and code != DateCode.SLASH:
            string += " "

    if return_strf:
        return string.strip()

    return now.strftime(string).strip()
