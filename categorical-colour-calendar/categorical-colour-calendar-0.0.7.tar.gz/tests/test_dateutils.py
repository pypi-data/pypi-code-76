from datetime import datetime

from dateutils import count_months, get_week_of_month


def test_get_week_of_month():
    assert (get_week_of_month(datetime(2021, 2, 1)) == 0)
    assert (get_week_of_month(datetime(2021, 2, 7)) == 0)

    assert (get_week_of_month(datetime(2021, 2, 8)) == 1)
    assert (get_week_of_month(datetime(2021, 2, 14)) == 1)

    assert (get_week_of_month(datetime(2021, 2, 15)) == 2)
    assert (get_week_of_month(datetime(2021, 2, 21)) == 2)

    assert (get_week_of_month(datetime(2021, 2, 22)) == 3)
    assert (get_week_of_month(datetime(2021, 2, 28)) == 3)

    assert (get_week_of_month(datetime(2021, 8, 1)) == 0)
    assert (get_week_of_month(datetime(2021, 8, 2)) == 1)


def test_count_months():
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 1)) == 1)
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 2)) == 1)
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 31)) == 1)

    assert (count_months(datetime(2021, 1, 1), datetime(2021, 2, 1)) == 2)
    assert (count_months(datetime(2021, 1, 31), datetime(2021, 2, 1)) == 2)
    assert (count_months(datetime(2021, 1, 31), datetime(2021, 2, 28)) == 2)

    assert (count_months(datetime(2021, 1, 31), datetime(2022, 1, 1)) == 13)
