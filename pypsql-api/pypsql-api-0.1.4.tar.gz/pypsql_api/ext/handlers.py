from typing import Tuple, Optional, Union, Any

from pandas import DataFrame

from pypsql_api.config.types import Session


class AuthHandler:

    def handle(self, session: Session) -> Tuple[bool, Optional[str]]:
        """
        :param session:
        :return: Tuple[bool, Optional[str]] if (true, any) then AuthOK, otherwise AuthFail, and the message in the str
        contains any error message
        """
        raise Exception("Not implemented")


class QueryHandler:

    def handle(self, session: Session, sql) -> Tuple[Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
        """
        :param session:
        :param sql: any sql statement passed by the client,
         this can be multiple statements and being-commit statements.
        :return: None -> No result
                 (Any, Msg)  -> Msg for future use to return notification messages.
                 (DataFrame, Any) -> The DataFrame the contains the data and schema returned
        """
        raise Exception("Not implemented")
