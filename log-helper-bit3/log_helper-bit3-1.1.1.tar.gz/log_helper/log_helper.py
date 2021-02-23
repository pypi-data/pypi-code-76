from datetime import datetime
from inspect import getframeinfo, stack, Traceback

from log_helper.models import LogModel


class LogHelper:
    CRITICAL: int = 50
    ERROR: int = 40
    DEBUG: int = 10
    FATAL: int = CRITICAL
    INFO: int = 20
    NOTSET: int = 0
    WARNING: int = 30
    WARN: int = WARNING

    def __init__(self):
        self.logs: list[LogModel] = []
        self.__logTypes: list[int] = [
            self.CRITICAL
            , self.ERROR
            , self.DEBUG
            , self.FATAL
            , self.INFO
            , self.NOTSET
            , self.WARNING
            , self.WARN
        ]

    def debug(self, message: str) -> None:
        """
        Registra un mensaje tipo DEBUG en el log

        :param message: Mensaje que se desea registrar
        :type message: str
        :return:
        """

        self.__add_log(self.DEBUG, message)

    def info(self, message: str) -> None:
        """
        Registra un mensaje tipo INFO en el log

        :param message: Mensaje que se desea registrar
        :type message: str
        :return:
        """

        self.__add_log(self.INFO, message)

    def warning(self, message: str) -> None:
        """
        Registra un mensaje tipo WARNING en el log

        :param message: Mensaje que se desea registrar
        :type message: str
        :return:
        """

        self.__add_log(self.WARNING, message)

    def error(self, message: str) -> None:
        """
        Registra un mensaje tipo ERROR en el log

        :param message: Mensaje que se desea registrar
        :type message: str
        :return:
        """

        self.__add_log(self.ERROR, message)

    def fatal(self, message: str) -> None:
        """
        Registra un mensaje tipo FATAL en el log

        :param message: Mensaje que se desea registrar
        :type message: str
        :return:
        """

        self.__add_log(self.FATAL, message)

    @DeprecationWarning
    def add_log(self, logType: int, message: str) -> None:
        """
        Agrega a la pila de logs un nuevo mensaje

        :param logType: Tipo de mensaje
        CRITICAL: int = 50
        FATAL: int = CRITICAL
        ERROR: int = 40
        WARNING: int = 30
        WARN: int = WARNING
        INFO: int = 20
        DEBUG: int = 10
        NOTSET: int = 0
        :type logType: int
        :param message: Mensaje que se desea registrar en el log
        :type message: str
        """

        if logType not in self.__logTypes:
            logType = self.NOTSET

        self.__add_log(logType, message)

    def __add_log(self, logType: int, message: str) -> None:
        """
        Agrega a la pila de logs un nuevo mensaje

        :param logType: Tipo de mensaje
        CRITICAL: int = 50
        FATAL: int = CRITICAL
        ERROR: int = 40
        WARNING: int = 30
        WARN: int = WARNING
        INFO: int = 20
        DEBUG: int = 10
        NOTSET: int = 0
        :type logType: int
        :param message: Mensaje que se desea registrar en el log
        :type message: str
        """

        if message is None or message.strip().__len__() == 0:
            return

        caller: Traceback = getframeinfo(stack()[1][0])
        log = LogModel()
        log.type_log = logType
        log.filename = caller.filename
        log.function = caller.function
        log.line_number = caller.lineno
        log.message = message.strip()
        log.creation_date = datetime.now()

        self.logs.append(log)
