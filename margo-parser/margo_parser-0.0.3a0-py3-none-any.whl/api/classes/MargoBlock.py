from ...tokenizer import tokenize
from .MargoStatement import MargoStatement
from .MargoAssignment import MargoAssignment
from .MargoDirective import MargoDirective
from typing import List


class MargoBlock:
    """A collection of Margo statements."""

    def __init__(self, source: str):

        """Parses source immediately, raising an exception if parsing
        fails.
        :param source: The source code string
        :raises: MargoParseException if the source string cannot be parsed
        :raises: MargoLangException if there's some other error"""

        # This is what raises the MargoParseException if it fails
        parsed = tokenize(source)
        self.__statements = []
        # TODO - Test statement for valid structure
        for statement in parsed["BODY"]:
            statement_type = statement["TYPE"]
            statement_name = statement["NAME"]
            if "VALUE" in statement:
                statement_value = statement["VALUE"]
                statement = MargoAssignment(
                    statement_name,
                    statement_value
                )
            else:
                statement = MargoDirective(statement_name)

            self.__statements.append(statement)

    @property
    def statements(self) -> List[MargoStatement]:
        """List of Margo statements"""
        return self.__statements