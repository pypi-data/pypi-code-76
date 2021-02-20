from tests.helpers.testbase import TestBase
from cerami.request.search_attribute import DictAttribute

class TestDictAttribute(TestBase):
    def setUp(self):
        self.attribute = DictAttribute()

    def test_add(self):
        """it updates the value"""
        self.attribute.add({'test': True})
        assert self.attribute.value == {'test': True}
        self.attribute.add({'test': False})
        assert self.attribute.value == {'test': False}

    def test_build(self):
        """returns the value"""
        self.attribute.add({'test': True})
        assert self.attribute.build() == {'test': True}

