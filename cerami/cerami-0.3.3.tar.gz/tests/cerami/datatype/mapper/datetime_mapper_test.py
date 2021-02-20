from mock import Mock, patch
from datetime import datetime, timezone
from tests.helpers.testbase import TestBase
from cerami.datatype import Datetime
from cerami.datatype.mapper import DatetimeMapper

class TestDatetimeMapper(TestBase):
    def setUp(self):
        self.dt = Datetime()
        self.mapper = DatetimeMapper(self.dt)

    def test_resolve(self):
        """it adds the utc timezone and calls isoformat"""
        val = Mock()
        mocked_utc_datetime = Mock()
        val.replace.return_value = mocked_utc_datetime
        mocked_utc_datetime.isoformat.return_value = "fake isostring"
        res = self.mapper.resolve(val)
        val.replace.assert_called_with(tzinfo=timezone.utc)
        assert res == "fake isostring"

    def test_parse(self):
        """it uses dateutil.parser.parse"""
        with patch('dateutil.parser.parse') as parser:
            parser.return_value = 'parsed'
            assert self.mapper.parse('2020-01-01T00:00:00Z') == 'parsed'
