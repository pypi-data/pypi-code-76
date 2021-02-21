import logging
from PyDoge.utils import concat


class Logger:
    def __init__(self, local=False):
        self.local = local
        if not local:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.INFO)

    def info(self, *message):
        msg = concat(message)
        if self.local:
            print(msg)
        else:
            self.logger.info(msg)
