from tests.helpers.testbase import TestBase
from cerami.request.search_attribute import SearchAttribute

class TestSearchAttribute(TestBase):
    def setUp(self):
        self.attribute = SearchAttribute("Test")

    def test_add(self):
        """it sets the value"""
        self.attribute.add(123)
        assert self.attribute.value == 123

    def test_build(self):
        """it returns the value"""
        self.attribute.add(123)
        assert self.attribute.build() == 123

