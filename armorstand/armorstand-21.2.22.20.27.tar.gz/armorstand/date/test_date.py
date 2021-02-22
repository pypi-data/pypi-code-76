from .date import DateCode
from .date import get_date


def test_get_date():
    assert (
        get_date(
            [DateCode.DAY, DateCode.MONTH, DateCode.COMMA, DateCode.YEAR],
            return_strf=True,
        )
        == "%-d %B, %Y"
    )

    assert (
        get_date(
            [
                DateCode.MONTH_NUMBER,
                DateCode.SLASH,
                DateCode.DAY,
                DateCode.SLASH,
                DateCode.SHORT_YEAR,
            ],
            return_strf=True,
        )
        == "%-m/%-d/%y"
    )
