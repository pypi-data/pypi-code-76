from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.decorators import primary_key

class TestPrimaryKey(TestBase):
    @primary_key('id')
    class SinglePartition(Model):
        id = String()

    @primary_key('id', 'name')
    class SortKeyModel(Model):
        id = String()
        name = String()

    def test_single_key(self):
        cls = self.SinglePartition
        assert cls._primary_key == (cls.id,)

    def test_sort_key(self):
        cls = self.SortKeyModel
        assert cls._primary_key == (cls.id, cls.name)
