import logging
import time
try:
    #from contextlib import AbstractAsyncContextManager
    from contextlib import AbstractContextManager
except ImportError:
    #AbstractAsyncContextManager = object
    AbstractContextManager = object
import typing as tp
from typing import Dict, Tuple, Union
from types import TracebackType

import fuglu.connectors.milterconnector as sm
import fuglu.connectors.asyncmilterconnector as asm
from fuglu.scansession import TrackTimings

from fuglu.connectors.milterconnector import (
    CONNECT,
    HELO,
    MAILFROM,
    RCPT,
    HEADER,
    EOH,
    EOB,
    ACCEPT,
    CONTINUE,
    DISCARD,
    TEMPFAIL,
    REJECT,
)
import fuglu.shared as fs

# conversion return code to Milter return code
retcode2milter = {
    fs.DUNNO: CONTINUE,
    fs.ACCEPT: ACCEPT,
    fs.DELETE: DISCARD,
    fs.REJECT: REJECT,
    fs.DEFER: TEMPFAIL,
}


class SumAsyncTime(AbstractContextManager):
    """Async context manager to additionally sum async await calls"""
    def __init__(self, timer: TrackTimings, key: tp.Optional[str] = None, logid: tp.Optional[str] = None):
        self.timer = timer
        self.asyncstart = None
        self.asyncend = None
        self.key = key
        self.logid = logid
        self.logger = logging.getLogger('fuglu.SumAsyncTime')

    def __enter__(self):
        self.asyncstart = time.time()
        #self.logger.debug(f"{self.logid} ({self.key}) -> enter with time {self.asyncstart}")

    def __exit__(self, exc_type: tp.Optional[tp.Type[BaseException]], exc_value: tp.Optional[BaseException], traceback: tp.Optional[TracebackType]):
        self.asyncend = time.time()
        #self.logger.debug(f"{self.logid} ({self.key}) -> exit with time {self.asyncend}")
        self.timer.sum_asynctime(self.asyncend - self.asyncstart, self.key, logid=self.logid)


class MilterSuspect:
    """Milter Suspect"""
    def __init__(self, id: str, values: Dict[str, str]):
        self.logger = logging.getLogger("Fuglu.MSuspect")
        # logger

        self.id = id
        self.values = values
        #all values offered by postfix (dict)


class BMPConnectMixin:
    """Basic Milter Plugin Mixing to implement plugin for connect state"""
    def examine_connect(self, sess: Union[sm.MilterSession, asm.MilterSession], host: str, addr: str) -> Union[bytes, Tuple[bytes, str]]:
        """Examine connect state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPHeloMixin:
    """Basic Milter Plugin Mixing to implement plugin for helo state"""
    def examine_helo(self, sess: Union[sm.MilterSession, asm.MilterSession], helo: str) -> Union[bytes, Tuple[bytes, str]]:
        """Examine helo state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPMailFromMixin:
    """Basic Milter Plugin Mixing to implement plugin for mailfrom state"""
    def examine_mailfrom(self, sess: Union[sm.MilterSession, asm.MilterSession], sender: str) -> Union[bytes, Tuple[bytes, str]]:
        """Examine mailfrom state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPRCPTMixin:
    """Basic Milter Plugin Mixing to implement plugin for rcpt state"""
    def examine_rcpt(self, sess: Union[sm.MilterSession, asm.MilterSession], recipient: str) -> Union[bytes, Tuple[bytes, str]]:
        """Examine recipient state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPHeaderMixin:
    """Basic Milter Plugin Mixing to implement plugin for header state"""
    def examine_header(self, sess: Union[sm.MilterSession, asm.MilterSession], key: bytes, value: bytes) -> Union[bytes, Tuple[bytes, str]]:
        """Examine header state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPEOHMixin:
    """Basic Milter Plugin Mixing to implement plugin for end-of-headers state"""
    def examine_eoh(self, sess: Union[sm.MilterSession, asm.MilterSession]) -> Union[bytes, Tuple[bytes, str]]:
        """Examine eoh state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BMPEOBMixin:
    """Basic Milter Plugin Mixing to implement plugin for end-of-body state"""
    def examine_eob(self, sess: Union[sm.MilterSession, asm.MilterSession]) -> Union[bytes, Tuple[bytes, str]]:
        """Examine eob state, return action code or tuple with action code and message"""
        raise NotImplementedError()


class BasicMilterPlugin(fs.BasicPlugin):
    """Base for milter plugins, derive from BMP***Mixins above to implement states"""

    ALL_STATES = {
        CONNECT: BMPConnectMixin,
        HELO: BMPHeloMixin,
        MAILFROM: BMPMailFromMixin,
        RCPT: BMPRCPTMixin,
        HEADER: BMPHeaderMixin,
        EOH: BMPEOHMixin,
        EOB: BMPEOBMixin,
    }

    def __init__(self, config, section=None):
        super().__init__(config, section=section)
        self.requiredvars.update({
            'state': {
                'default': '',
                'description': f'comma/space separated list states this plugin should be '
                               f'applied ({",".join(BasicMilterPlugin.ALL_STATES.keys())})'
            }
        })
        self._state = None
        self.logger = self._logger()

    @property
    def state(self):
        if self._state is None:
            self._state = [s.lower() for s in fs.Suspect.getlist_space_comma_separated(self.config.get(self.section, 'state'))]
        return self._state

    def lint(self, **kwargs) -> bool:
        if not super().lint():
            return False

        checkstates = kwargs.get('state', self.state)
        if isinstance(checkstates, str):
            checkstates = [checkstates]

        if not all(s in BasicMilterPlugin.ALL_STATES.keys() for s in checkstates):
            print("Error: Not all states are available/implemented")
            print(f"checkstates: {checkstates}")
            print(f"allkeys: {list(BasicMilterPlugin.ALL_STATES.keys())}")
            return False

        for s in checkstates:
            cls = BasicMilterPlugin.ALL_STATES[s]
            if not isinstance(self, cls):
                print(f"ERROR: {self.__class__.__name__} does not implement {cls.__name__}")
                return False

        return True

    def _logger(self):
        """returns the logger for this plugin"""
        myclass = self.__class__.__name__
        loggername = "fuglu.mplugin.%s" % myclass
        return logging.getLogger(loggername)