from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.request.search_attribute import SearchAttribute
from cerami.request.mixins import Limitable

class TestRequest(Limitable):
    pass

class TestLimitable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    def test_limit(self):
        """ it adds Limit"""
        self.request.add_attribute = Mock()
        self.request.limit(1)
        self.request.add_attribute.assert_called_with(
            SearchAttribute,
            'Limit',
            1)
