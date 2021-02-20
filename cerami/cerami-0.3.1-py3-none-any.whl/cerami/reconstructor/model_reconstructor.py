from .base_reconstructor import BaseReconstructor

class ModelReconstructor(BaseReconstructor):
    """A Reconstructor class to convert the DynamoDB response data back into a Model"""

    def __init__(self, model_cls):
        """constructor for ModelReconstructor

        Parameters:
            model_cls: the class of the Model to convert the data into
        """
        self.model_cls = model_cls

    def reconstruct(self, item_dict):
        """Convert the item_dict into a Model instance

        Iterates over all columns in the model_cls and tries to set the value based on the
        item_dict's keys

        Parameters:
            item_dict: a dict from DynamoDB. It will be in the format like
                ``{"a_column": {"S": "my_value"}}``
        Returns:
            an instance of ``model_cls``
        """
        data = {}
        for column in self.model_cls._columns:
            try:
                val = item_dict[column.column_name]
            except KeyError:
                continue
            data[column.column_name] = column.mapper.reconstruct(val)
        return self.model_cls(**data)
