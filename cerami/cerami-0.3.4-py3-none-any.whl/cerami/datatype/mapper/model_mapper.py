from .base_datatype_mapper import BaseDatatypeMapper

class ModelMapper(BaseDatatypeMapper):
    """A Mapper class for converting Models to DynamoDB dictionaries

    The ModelMapper must be initialized with a ModelMap datatype. It depends on the
    model_cls attribute to know which columns and datatypes to use.

    The benefit of using a ModelMapper over a DictMapper is there is no guess work.
    Because all columns are defined, it automatically knows the datatypes to use.

    For example::

        child = Child(gender="female", age=2)
        mapper = ModelMapper(ModelMap(model_cls=Child))
        mapper.map(child)
        {
            "M": {
                "gender": {
                    "S": "female"
                },
                "age": {
                    "N": "2"
                },
                "name": {
                    "NULL": True,
                },
            }
        }

        mapper.parse({"M": {"name": {"S": "Baby"}}})
        <Child object>
    """

    def resolve(self, value):
        """Convert the model into a DynamoDB formatted dictionary

        Any values column values that are not set on the instance being mapped will
        automatically set the ``{"NULL": True}`` for that column

        Parameters:
            value: the model to be converted

        Returns:
            a dictionary where each key is a column of the model and the value is the
            mapped version of the column value
        """
        res = {}
        model_cls = self.datatype.model_cls
        for column in model_cls._columns:
            column_datatype = getattr(model_cls, column.column_name)
            column_value = getattr(value, column.column_name, None)
            res[column.column_name] = column_datatype.mapper.map(column_value)
        return res

    def parse(self, value):
        """Convert the DynamoDB dict into an instance of the model

        Iterate over all columns on the Model. Use the columns mapper to reconstruct
        the value.

        Parameters:
            value: a dictionary where each key represents a column of the model as a 
                DynamoDB formatted dictionary

        Returns:
            an instance of the model class
        """
        data = {}
        model_cls = self.datatype.model_cls
        for column in model_cls._columns:
            try:
                val = value[column.column_name]
            except KeyError:
                continue
            data[column.column_name] = column.mapper.reconstruct(val)
        return model_cls(**data)
