import numbers
from copy import deepcopy
from .number import Number
from .string import String
from .set import Set
from .base_datatype import DynamoDataType
from .expression import ListAppendExpression
from .mapper import (
    DictMapper,
    ListMapper)

class DefaultMapGuesser(object):
    """A class to guess what datatype to send to DynamoDB based the attribute value

    A generic map or list type can have anything as its keys and values. There is no way
    to know what the Datatypes should be used for certainty because many of the datatypes
    defined (like Datetimes) all are converted to a String before saved in the table.
    This class will look at the values and decide which Datatype to use.

    This class can be extended to handle your specific use cases. For example, if you know
    that the key "my_datetime" should always return a Datetime datatype, the guess()
    method can be overridden to handle specific cases.
    """

    def guess(self, key, value):
        """guess the datatype from the value

        Guessing for mapping means we are trying to figure out the datatype
        in order to convert it into a dict usable by dynamodb. So this
        guesser will makes its guess based on value directly

        Parameters:
            key: the string of the column_name
            value: the value of the column_name

        Returns:
            A DynamoDataType object
        """
        if isinstance(value, numbers.Number):
            return Number()
        elif isinstance(value, dict):
            return Map()
        elif isinstance(value, list):
            return List()
        else:
            return String()


class DefaultParseGuesser(object):
    """A class to decide what datatype to use toe

    A generic map or list type can have anything as its keys and values. There is no way
    to know what the Datatypes should be used for certainty because many of the datatypes
    defined (like Datetimes) all are converted to a String before saved in the table.
    This class will look at the condition_type to determine what Datatype should be used

    This class can be extended to handle your specific use cases. For example, if you know
    that the key "my_datetime" should always return a Datetime datatype, the guess()
    method can be overridden to handle specific cases.
    """

    def guess(self, key, value):
        """guess the datatype from the key within value

        we are guessing on something like {'M': {'test': {'S': 'hello'}}}
        where key is 'test' and value is {'S': 'hello'}
        this will fetch the inner key ('S') and guess from this value

        Parameters:
            key: the column_name of the attribute
            value: a dict whose key is the condition_type and value is the value
                of the column.

        Returns:
        A DynamoDataType object

        Example:
        guess('my_string', {'S': 'hello'})
        """
        attr_key = list(value)[0]
        if attr_key == "N":
            return Number()
        elif attr_key == "S":
            return String()
        elif attr_key == "SS":
            return Set(String())
        elif attr_key == "NS":
            return Set(Number())
        elif attr_key == "L":
            return List()
        elif attr_key == "M":
            return Map()
        else:
            return String()


class Map(DynamoDataType):
    """A class to represent generic Map datatypes

    A Map is used to store nested data within a record. It is essentially a dict where
    each key/value is stored in the database. Since the values can be anything, a
    MapGuesser and ParseGuesser are used to determine the datatype of these nested
    attributes. These guessers are passed to the constructor, and can be customized to
    return specific datatypes if you know the structure of the nested objects.
    """

    def __init__(
            self,
            map_guesser=None,
            parse_guesser=None,
            default=None,
            column_name=""):
        """constructor for Map

        Parameters:
            map_guesser: an object inheriting from DefaultMapGuesser
                Defaults to the DefaultMapGuesser
            parse_guesser: an object inheriting from DefaultParseGuesser
                Defaults to the DefaultParseGuesser.
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
        """
        super(Map, self).__init__(
            condition_type="M",
            default=default,
            column_name=column_name)
        self.map_guesser = map_guesser or DefaultMapGuesser()
        self.parse_guesser = parse_guesser or DefaultParseGuesser()
        self.mapper = DictMapper(self, self.map_guesser, self.parse_guesser)

    def key(self, datatype, key):
        """build a duplicate datatype with the column_name using a dot notiation

        When forming a Request that involves a specific key from the Map, that item can
        be specified using the key() method.

        Parameters:
            datatype: a DynamoDataType instance representing the nested value
            key: the name of the nested value

        Returns:
            A copy of the datatype with an new keyname

        For example::

            Parent.scan.filter(MyModel.child.key(String(), 'name') == 'Zac')
        """
        column_name = self.column_name + "." + key
        return type(datatype)(column_name=column_name)


class List(DynamoDataType):
    """A class to represent generic List datatypes

    A List is used to store a collection of values of a varying length. It is essentially
    an array where each item is the value stored in the database. Since values can be
    anything, a MapGueser and ParseGuesser are used to determine the datatype of the
    array's items. These guessers are passed to the constructor, and can be customized to
    return specific datatypes if you know the structure of the array and each item.
    """
    def __init__(
            self,
            map_guesser=None,
            parse_guesser=None,
            default=None,
            column_name=""):
        """constructor for List

        Parameters:
            map_guesser: An object inheriting from DefaultMapGuesser
                Defaults to the DefaultMapGuesser
            parse_guesser: An object inheriting from DefaultParseGuesser
                Defaults to the DefaultParseGuesser.
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
        """
        super(List, self).__init__(
            condition_type="L",
            default=default,
            column_name=column_name)
        self.map_guesser = map_guesser or DefaultMapGuesser()
        self.parse_guesser = parse_guesser or DefaultParseGuesser()
        self.mapper = ListMapper(self, self.map_guesser, self.parse_guesser)

    def append(self, array):
        """Build an expression to add the array to the end of the existing column data

        It can only be used in SET UpdateExpressions.

        Parameters:
            array: can be a list or single value to be appended. When it is a single
                value, it is automatically put inside its own array, before building the
                expression.

        Returns:
            A ListAppendExpression

        For example::

            Person.update \\
                .key(Person.email == "test@test.com")
                .set(Person.toys.append({"color": "red", "name": "car"})
        """
        if not isinstance(array, list):
            array = [array]
        return ListAppendExpression(self, array)

    def index(self, idx, datatype):
        """build a duplicate datatype with the _index set to idx

        When forming a Request that involves a specific item in the List, that item can
        be specified using this index() method.

        Parameters:
            idx: a number for the index of the desired item in the list
            datatype: a DynamoDataType object representing the item indexed

        Returns:
            A copy of the datatype with _index set

        Raises:
            ValueError: An error when the datatype is not an instance of DynamoDataType

        For example::

            MyModel.scan.filter(MyModel.my_list.index(1, String()) == 'world')
        """
        if not isinstance(datatype, DynamoDataType):
            raise ValueError("datatype must be an instance of DynamoDataType")
        dt = deepcopy(datatype)
        dt._index = idx
        return dt
