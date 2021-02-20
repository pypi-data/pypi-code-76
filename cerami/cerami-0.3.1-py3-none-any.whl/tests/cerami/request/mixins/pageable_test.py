from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.request.mixins import Pageable
from cerami.request.search_attribute import DictAttribute

class TestRequest(Pageable):
    pass

class TestPageable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    def test_start_key(self):
        """it adds the dict to as ExclusiveStartKey"""
        self.request.add_attribute = Mock()
        self.request.start_key({'fakeDict': True})
        self.request.add_attribute.assert_called_with(
            DictAttribute,
            'ExclusiveStartKey',
            {'fakeDict': True})
