from ...exceptions import MargoLangException
from abc import ABC

class MargoStatementTypes:

    """Supported types of Margo statements"""

    DECLARATION = "DECLARATION"
    DIRECTIVE = "DIRECTIVE"

    VALID_TYPES = [DECLARATION, DIRECTIVE]

    @staticmethod
    def is_valid_type(statement_type: str) -> bool:
        """Determine if a string is a valid margo statement type"""
        return statement_type in MargoStatementTypes.VALID_TYPES


class MargoStatement(ABC):

    """A Margo statement"""

    def __init__(self, statement_type: str, name: str, value=None):

        """
        :param statement_type: MargoStatementTypes.DECLARATION or MargoStatementTypes.DIRECTIVE
        :param name: the name of the statement
        :param value: the value of the statement
        @raises MargoLangException if parameters are invalid
        """

        if not MargoStatementTypes.is_valid_type(statement_type):
            raise MargoLangException("Invalid Margo statement type: " + statement_type)
        self.__type = statement_type
        if type(name) != str:
            raise MargoLangException("Margo statement name type must be str")
        self.__name = name
        # Value can be anything, so don't validate
        if self.__type == MargoStatementTypes.DIRECTIVE and value is not None:
            raise MargoLangException("Cannot create a directive with value")
        self.__value = value

    @property
    def name(self) -> str :
        """The name of the statement""" 
        return self.__name
     
    @property
    def type(self) -> str:
        """'DIRECTIVE' or 'DECLARATION'"""
        return self.__type

    @property
    def value(self) -> any:
        """Any value. Should be None for directives"""
        return self.__value