from copy import copy
from .base_datatype import DynamoDataType
from .mapper import ModelMapper

class ModelMap(DynamoDataType):
    """A class to represent a nested model as a Map

    A ModelMap automatically sets the column_names to use the dot notation when accessing
    the nested attributes. This allows direct reference to nested keys when making
    requests. For example::

        Parent.scan.filter(Parent.child.name == 'Zac')
    """

    def __init__(self, model_cls, mapper_cls=ModelMapper, column_name=""):
        """constructor for ModelMap

        Parameters:
            model_cls: the class of the nested Model being used
            mapper_cls: A mapper class to manipulate data to/from dynamodb.
                Defaults to the ModelMapper
            column_name: a string defining the name of the column on the table
        """
        super(ModelMap, self).__init__(
            condition_type="M",
            mapper_cls=mapper_cls,
            column_name=column_name)
        self.model_cls = model_cls
        for column in self.model_cls._columns:
            setattr(self, column.column_name, copy(column))

    def set_column_name(self, val):
        """Update the column_name of this instance.

        Automatically apply a dot notation chain from the this column_name to
        all of the nested models datatypes column_names

        Parameters:
            val: the name of the column
        For example::

            class Child(object):
                name = String()

            class Parent(db.Model):
                child = ModelMap(Child)

            Parent.child.name.column_name # <== 'child.name'
        """
        super(ModelMap, self).set_column_name(val)
        for name, attr in self.__dict__.items():
            if isinstance(attr, DynamoDataType):
                new_name = val + "." + name
                attr.set_column_name(new_name)
