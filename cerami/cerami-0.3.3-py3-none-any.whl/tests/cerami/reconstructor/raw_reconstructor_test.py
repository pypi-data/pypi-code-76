from tests.helpers.testbase import TestBase
from cerami.reconstructor import RawReconstructor

class TestRawReconstructor(TestBase):
    def setUp(self):
        self.reconstructor = RawReconstructor()

    def test_reconstruct(self):
        """it returns the item"""
        item = {'test': True}
        res = self.reconstructor.reconstruct(item)
        assert res == item

