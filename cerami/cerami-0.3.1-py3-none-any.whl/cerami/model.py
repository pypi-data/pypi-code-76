from .datatype import DynamoDataType
from .data_attribute import DynamoDataAttribute
from .reconstructor import ModelReconstructor
from .request.return_values import ALL_NEW
from .request import (
    GetRequest,
    ScanRequest,
    PutRequest,
    UpdateRequest,
    DeleteRequest,
    QueryRequest)


class ModelMeta(type):
    """The meta class for all Models

    This meta class is automatically sets the column names on every column attribute
    and defines some class level properties for generating requests

    Attributes:
        _columns: An array for accessing all datatypes defined on the Model
    """
    def __new__(cls, clsname, bases, dct):
        """override the class creation

        Add the _columns property and define the column_name for each datatype
        """
        dct["_columns"] = []
        for name, val in dct.items():
            if isinstance(val, DynamoDataType):
                val.set_column_name(name.lower())
                dct["_columns"].append(val)
        return super(ModelMeta, cls).__new__(cls, clsname, bases, dct)

    @property
    def get(cls):
        """Create a GetRequest for the Model

        Returns:
            a GetRequest object
        """
        return GetRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))

    @property
    def scan(cls):
        """Create a ScanRequest for the Model

        Returns:
            a ScanRequest object
        """
        return ScanRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))

    @property
    def query(cls):
        """Create a QueryRequest for the Model

        Returns:
            a QueryRequest object
        """
        return QueryRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))

    @property
    def put(cls):
        """Create a PutRequest for the Model

        Returns:
            a PutRequest object
        """
        return PutRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))

    @property
    def update(cls):
        """Create an `UpdateRequest` for the Model

        Returns:
            an UpdateRequest object
        """
        update = UpdateRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))
        return update.returns(ALL_NEW)


    @property
    def delete(cls):
        """Create a `DeleteRequest` for the Model

        Returns:
            a DeleteRequest object
        """
        return DeleteRequest(
            cls.client,
            tablename=cls.__tablename__,
            reconstructor=ModelReconstructor(cls))

class Model(object, metaclass=ModelMeta):
    """This is the base class for all models.

    It automatically uses the `ModelMeta` to define properties for interacting with
    DynamoDB tables. It should be used to create all classes that need make requests
    to DynamoDB.

    Models consist of a series of DynamoDataTypes that define which columns are to be
    saved in the database. Each datatype is also an instance variable that can be
    manipulated through any methods defined on helper methods.

    For example::

        from cerami.decorators import primary_key
        from cerami.datatype import String

        @primary_key("email")
        class Person(Model):
           __tablename__ = "people"

           email = String()
           name = Sting()

        person = Person(email="test@test.com", name="Mom")
    """
    def __init__(self, **data_kwargs):
        """set all column values from data

        It will set any value not present in data but part of
        the models columns to None

        Parameters:
            **data_kwargs: Each kwarg should be the name of one of the columns with a 
                corresponding value
        """
        data = data_kwargs or {}
        data_keys = data.keys()
        for column in self._columns:
            name = column.column_name
            value = data.get(name, None)
            data_exists = name in data or column.default
            attr = DynamoDataAttribute(column, value, initialized=data_exists)
            setattr(self, name, attr)

    def __getattribute__(self, key, full=False):
        """override __getattribute__

        most of the time we want to call attr.get() when accessing a DynamoDataAttribute.
        The full flag can be used to get the actual object.
        """
        attr = super(Model, self).__getattribute__(key)
        if isinstance(attr, DynamoDataAttribute) and not full:
            return attr.get()
        else:
            return attr

    def __setattr__(self, key, value):
        attr = self._get_full_attribute(key)
        if isinstance(attr, DynamoDataAttribute):
            attr.set(value)
        else:
            super(Model, self).__setattr__(key, value)

    def _get_full_attribute(self, key):
        """Get the class-level DynamoDataType object"""
        try:
            return self.__getattribute__(key, full=True)
        except AttributeError:
            return None

    def as_item(self):
        """return all data values in a format for dynamodb

        Returns:
            a dictionary of the model in a format recognized by DynamoDB

        For example::

            person = Person(email="test@test.com", name="Mom")
            person.as_item()
            {'email': {'S': 'test@test.com'}, 'name': {'S': 'Mom'}}
        """
        item = {}
        for column in self._columns:
            name = column.column_name
            attr = self._get_full_attribute(name)
            item[name] = column.mapper.map(attr.value)
        return item

    def delete(self):
        """delete this record from the database

        Automatically perform a `DeleteRequest` based on the model's primary key

        Returns:
            a DeleteResponse
        """
        deleter = self.__class__.delete
        for column in self._primary_key:
            column_name = column.column_name
            deleter = deleter.key(column == getattr(self.data, column_name))
        return deleter.execute()

    def put(self):
        """add this record to the database

        Automatically perform a `PutRequest` with the objects data

        Returns:
            a SaveResponse
        """
        putter = self.__class__.put
        putter.item(self.as_item())
        return putter.execute()

    def update(self):
        """update this record in the database

        Automatically perform an `UpdateRequest` based on the models attributes. It will
        only update columns that have been initialized or changed.

        Returns:
            a SaveResponse
        """
        updater = self.__class__.update
        for column in self._primary_key:
            column_name = column.column_name
            updater.key(column == getattr(self, column_name))
        for column in self._columns:
            column_name = column.column_name
            attr = self._get_full_attribute(column_name)
            if (not column in self._primary_key
                and (attr.initialized or attr._changed)):
                updater = updater.set(column, attr.value)
        return updater.execute()
