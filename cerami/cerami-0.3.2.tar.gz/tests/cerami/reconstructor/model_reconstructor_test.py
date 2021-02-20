from tests.helpers.testbase import TestBase
from cerami.reconstructor import ModelReconstructor
from cerami.model import Model
from cerami.datatype import String

class TestModelReconstructor(TestBase):
    class TestModel(Model):
        __tablename__ = 'test'
        _id = String()
        test = String()

    def setUp(self):
        self.reconstructor = ModelReconstructor(self.TestModel)

    def test_reconstruct(self):
        """it calls parse for each column"""
        data = {'_id': {'S': '123'}, 'test': {'S': 'cool'}}
        res = self.reconstructor.reconstruct(data)
        assert isinstance(res, self.TestModel)
        assert res._id == '123'
        assert res.test == 'cool'

    def test_reconstruct_missing_key(self):
        """it skips missing columns"""
        data = {'test': {'S': 'cool'}}
        res = self.reconstructor.reconstruct(data)
        assert isinstance(res, self.TestModel)
        assert res._id == None
        assert res.test == 'cool'

