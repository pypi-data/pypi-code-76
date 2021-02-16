import pytest
import re
from runeatest import utils


def test_get_date_and_time():
    actual = utils.get_date_and_time()
    actual_date = actual[0]
    actual_time = actual[1]
    assert re.match("[\\d]{4}-[\\d]{1,2}-[\\d]{1,2}", actual_date)
    assert re.match("[\\d]{1,2}:[\\d]{1,2}:[\\d]{1,2}", actual_time)
