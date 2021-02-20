from mock import Mock, patch
from datetime import datetime, timezone
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype.expression import (
    EqualityExpression,
    InExpression,
    ListAppendExpression,
    ArithmeticExpression)
from cerami.datatype.mapper import (
    ByteMapper,
    StringMapper,
    ModelMapper,
    DictMapper,
    ListMapper,
    IntegerMapper,
    DecimalMapper,
    DatetimeMapper,
    SetMapper)
from cerami.datatype import (
    DynamoDataType,
    BaseString,
    BaseNumber,
    ByteBuffer,
    String,
    Datetime,
    Map,
    ModelMap,
    List,
    Set)

class TestBaseString(TestBase):
    def setUp(self):
        super(TestBaseString, self).setUp()
        self.dt = BaseString(column_name="test")

    def test_condition_type(self):
        assert self.dt.condition_type == "S"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, StringMapper)

class TestBaseNumber(TestBase):
    def setUp(self):
        super(TestBaseNumber, self).setUp()
        self.dt = BaseNumber(column_name="test")

    def test_condition_type(self):
        assert self.dt.condition_type == "N"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, IntegerMapper)

    def test_add(self):
        """it returns an ArithmeticExpression"""
        res = self.dt.add(5)
        assert isinstance(res, ArithmeticExpression)
        assert res.expression == '+'

    def test_subtract(self):
        """it returns an ArithmeticExpression"""
        res = self.dt.subtract(5)
        assert isinstance(res, ArithmeticExpression)
        assert res.expression == '-'

class TestString(TestBase):
    def setUp(self):
        super(TestString, self).setUp()
        self.dt = String(column_name="test")

    def test_condition_type(self):
        assert self.dt.condition_type == "S"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, StringMapper)

class TestByteBuffer(TestBase):
    def setUp(self):
        super(TestByteBuffer, self).setUp()
        self.dt = ByteBuffer(column_name="test")

    def test_condition_type(self):
        assert self.dt.condition_type == "B"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, ByteMapper)

class TestDatetime(TestBase):
    def setUp(self):
        super(TestDatetime, self).setUp()
        self.dt = Datetime(column_name="test")

    def test_condition_type(self):
        assert self.dt.condition_type == "S"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, DatetimeMapper)

class TestMap(TestBase):
    def setUp(self):
        super(TestMap, self).setUp()
        self.mocked_guesser = Mock()
        self.dt = Map(
            map_guesser=self.mocked_guesser,
            parse_guesser=self.mocked_guesser)

    def test__init__(self):
        """it initializes the guesser"""
        assert self.dt.map_guesser == self.mocked_guesser
        assert self.dt.parse_guesser == self.mocked_guesser

    def test_condition_type(self):
        assert self.dt.condition_type == "M"

    def test_mapper(self):
        """it is an instance of DictMapper"""
        assert isinstance(self.dt.mapper, DictMapper)

class TestList(TestBase):
    def setUp(self):
        super(TestList, self).setUp()
        self.mocked_guesser = Mock()
        self.dt = List(
            column_name="test",
            map_guesser=self.mocked_guesser,
            parse_guesser=self.mocked_guesser)

    def test__init__(self):
        """it sets guesser"""
        assert self.dt.map_guesser == self.mocked_guesser
        assert self.dt.parse_guesser == self.mocked_guesser

    def test_property(self):
        assert self.dt.condition_type == "L"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, ListMapper)

    def test_append(self):
        """it should return a ListAppendExpression"""
        res = self.dt.append(['Test'])
        assert isinstance(res, ListAppendExpression)
        assert res.value == ['Test']

    def test_append_scalar(self):
        """it converts the value to a list when it isnt one"""
        res = self.dt.append('Test')
        assert isinstance(res, ListAppendExpression)
        assert res.value == ['Test']

    def test_index(self):
        """it returns a new instance of the datatype passed with the column_name
        it sets _index on the returned datatype instance"""
        res = self.dt.index(0, String())
        assert isinstance(res, String)
        assert res._index == 0

    def test_index_throws_ValueEreror(self):
        """it throws a ValueError when the datatype is not an instance
        This is to prevent people from accidentially passing the class in and breaking
        everything
        """
        self.assertRaises(ValueError, self.dt.index, 0, String)

class TestModelMap(TestBase):
    class TestModel(Model):
        __tablename__ = "test"
        test1 = String()
        test2 = String()

    def setUp(self):
        super(TestModelMap, self).setUp()
        self.dt = ModelMap(self.TestModel, column_name="test")

    def test__init__(self):
        """it should setattr for each column in the model_cls"""
        for column in self.TestModel._columns:
            assert hasattr(self.dt, column.column_name)
            assert isinstance(getattr(self.dt, column.column_name),
                              type(column))

    def test_condition_type(self):
        assert self.dt.condition_type == "M"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, ModelMapper)

    def set_column_name(self):
        """it updates the column_name and all nested column names"""
        new_name = "test2"
        self.dt.set_column_name(new_name)
        assert self.dt.column_name == new_name
        for column in TestModel._columns:
            nested_column = getattr(self.dt, column.column_name)
            new_nested_name = new_name + "." + column.column_name
            assert nested_column.column_name == new_nested_name

class TestSet(TestBase):
    def setUp(self):
        super(TestSet, self).setUp()
        self.dt = Set(String(), column_name="test")

    def test_has_a_datatype(self):
        assert isinstance(self.dt.datatype, String)

    def test_condition_type(self):
        """it adds an S to the datatype's condition_type"""
        assert self.dt.condition_type == "SS"

    def test_mapper(self):
        assert isinstance(self.dt.mapper, SetMapper)

class TestDynamoDataType(TestBase):
    def setUp(self):
        super(TestDynamoDataType, self).setUp()
        self.dt = DynamoDataType(column_name="test")
        self.dt.mapper = StringMapper(self.dt)
        self.dt.condition_type = "S"

    def test__eq__(self):
        res = self.dt == 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == "="

    def test__ne__(self):
        res = self.dt != 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == "<>"

    def test__gt__(self):
        res = self.dt > 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == ">"

    def test__ge__(self):
        res = self.dt >= 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == ">="

    def test__lt__(self):
        res = self.dt < 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == "<"

    def test__le__(self):
        res = self.dt <= 1
        assert isinstance(res, EqualityExpression)
        assert res.expression == "<="

    def test_in_(self):
        res = self.dt.in_('1','2','3')
        assert isinstance(res, InExpression)
