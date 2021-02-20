from copy import deepcopy
from .dynamic import List
from .mapper import UniformListMapper

class UniformList(List):
    """A class to represent Lists of entirely the same datatype

    The Base List class uses a Guesser to try and determine the datatype to use for
    the each item in the array. A UniformList does not need to guess, since the
    datatype is consistent and stored as an attribute
    """
    def __init__(self, datatype, default=None, column_name=""):
        """constructor for UniformList

        Parameters:
            datatype: Any DynamoDataType that each item in the List will be
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
        """
        super(UniformList, self).__init__(default=default, column_name=column_name)
        self.datatype = datatype
        self.mapper = UniformListMapper(self.datatype.mapper)

    def index(self, idx):
        """build a duplicate datatype with the _index set to idx

        When forming a Request that involves a specific item in the UniformList,
        that item can be specified using this index() method

        Parameters:
            idx: a number for the index of the desired item in the list

        Returns:
            A copy of the datatype with _index set

        For example::

            MyModel.scan.filter(MyModel.number_list.index(2) == 100).execute()
        """
        dt = deepcopy(self.datatype)
        dt._index = idx
        return dt
