from .base_reconstructor import BaseReconstructor

class RawReconstructor(BaseReconstructor):
    """A Reconstructor class to return the data back exactly as it was given"""

    def reconstruct(self, item_dict):
        """Return the item_dict

        Parameters:
            item_dict: a dict from DynamoDB. It will be in the format like
                ``{"a_column": {"S": "my_value"}}``

        Returns:
            the item_dict passed in
        """
        return item_dict
