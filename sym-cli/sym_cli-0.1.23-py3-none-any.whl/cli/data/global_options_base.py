import inspect
import logging
from dataclasses import dataclass, replace
from typing import Sequence


@dataclass
class GlobalOptionsBase:
    debug: bool = False

    def clone(self, **kwargs):
        return replace(self, **kwargs)

    def dprint(self, *s: Sequence[str], **kwargs):
        s = list(map(str, filter(None, s)))
        if (s or kwargs) and self.debug:
            message = " ".join(s)
            if kwargs:
                message += ": " + ",".join([f"{k}={v}" for k, v in kwargs.items()])
            mod = inspect.getmodule(inspect.stack()[1][0])
            logging.getLogger(mod.__name__ if mod else __name__).info(message)
