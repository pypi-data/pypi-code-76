import cerami.datatype as dt
from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.reconstructor import ModelReconstructor
from cerami.data_attribute import DynamoDataAttribute
from cerami.request import (
    GetRequest,
    UpdateRequest,
    QueryRequest,
    ScanRequest)
from cerami import Cerami
from cerami.model import Model


class TestModelClass(TestBase):
    class DummyModel(Model):
        __tablename__ = "test"
        client = Mock()
        _id = dt.String()
        name = dt.String()
        tags = dt.Set(dt.String())

    def setUp(self):
        super(TestModelClass, self).setUp()
        self.model = self.DummyModel(_id='1', name='test')

    def test__new__(self):
        """All Model columns should have a column_name"""
        assert self.DummyModel._id.column_name == "_id"
        assert self.DummyModel.name.column_name == "name"

    def test__column(self):
        """it chould only return the DataTypes on the Schema"""
        idColumn = dt.String()
        testColumn = dt.String()
        class TestModel(Model):
            _id = idColumn
            test = testColumn
        assert len(TestModel._columns) == 2
        assert idColumn in TestModel._columns
        assert testColumn in TestModel._columns


    def test_put_calls_put(self):
        """put should call PutInterface.execute with the data as an item"""
        with patch('cerami.request.put_request.PutRequest.execute') as execute,\
            patch('cerami.request.put_request.PutRequest.item') as item:
            self.model.put()
            item.assert_called_with(self.model.as_item())
            execute.assert_called()

    def test_has_scan_property(self):
        """the class should have a ScanRequest"""
        assert isinstance(self.DummyModel.scan, ScanRequest)
        assert isinstance(self.DummyModel.scan.reconstructor, ModelReconstructor)

    def test_has_query_property(self):
        """the class should have a QueryRequest"""
        assert isinstance(self.DummyModel.query, QueryRequest)
        assert isinstance(self.DummyModel.query.reconstructor, ModelReconstructor)

    def test_has_update_property(self):
        """the class should have an UpdateRequest"""
        assert isinstance(self.DummyModel.update, UpdateRequest)
        assert isinstance(self.DummyModel.update.reconstructor, ModelReconstructor)

    def test_has_get_property(self):
        """the class should have a GetRequest"""
        assert isinstance(self.DummyModel.get, GetRequest)
        assert isinstance(self.DummyModel.get.reconstructor, ModelReconstructor)

    def test_init_sets_attributes(self):
        """it sets all keys in the model"""
        for column in self.model._columns:
            assert hasattr(self.model, column.column_name)


    def test__getattribute__(self):
        """it should return the value passed normally"""
        model = self.DummyModel(_id='abc')
        assert model._id == 'abc'

    def test__getattribute__full(self):
        """it should return the DynamoDataAttribute when full is true"""
        res = self.model.__getattribute__('_id', full=True)
        assert isinstance(res, DynamoDataAttribute)

    def test__setattr__(self):
        """it should call DynamoDataAttribute.set"""
        with patch("cerami.data_attribute.DynamoDataAttribute.set") as setter:
            self.model._id = "new_id"
            setter.assert_called()

    def test_get_full_attribute_none(self):
        """it should return None when the key is missing"""
        assert self.model._get_full_attribute('bad') is None
