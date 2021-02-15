# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import datetime
import logging
import os.path

from bs_lib.Pod   import Pod

from bs_loco.xloco import xLoco

from bs_loco.db.tables      import tMsg

from .provider_email import ProviderEmail


class LogfileEmail(ProviderEmail):
    """
    This is the logfile email provider.
    """
    LOG_FORMAT       = '[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s'
    CONSOLE_FORMAT   = '%(message)s '
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        """
        Constructor.
        """
        ProviderEmail.__init__(self)
        self._logfile = None


    def id(self) -> str:
        """
        Overload.
        """
        return 'logfile'


    def initialize(self, pod: Pod, dao: object, cfg: dict):
        """
        Overload.
        """
        ProviderEmail.initialize(self, pod, dao, cfg)

        self._logfile = self._init_logger(cfg)


    def destroy(self):
        """
        Overload.
        """
        self._logfile = None
        ProviderEmail.destroy(self)


    def _provider_send(self, payload: dict, res_list: list, msg: tMsg, addr_list: list) -> tuple:
        """
        Overload.
        """
        try:
            dt_start = datetime.datetime.now()

            self._logfile.info('Sending Email [msg:%d, to:%s]:' % (msg.id, str(addr_list)))
            self._logfile.info('  - Subject    : %s' % (payload['subject']))
            self._logfile.info('  - Html Body  : %s' % (payload['body-html']))
            self._logfile.info('  - Text Body  : %s' % (payload['body-text']))

            if res_list:
                self._logfile.info('  - Attachments')

                for r in res_list:
                    self._logfile.info('      %s' % (str(r)))

            dt_end = datetime.datetime.now()

        except Exception as x:
            self._log.error('Exception caught sending email [%s]' % (str(msg)))
            self._log.exception(x)
            return (False, None, str(x))

        return (True, dt_end - dt_start, None)


    def _init_logger(self, cfg: dict):
        """
        Initialize the logger object.

        :param cfg: The config.
        """
        if not cfg.get('path'):
            raise xLoco('Invalid config, [path] not set [provider:%s, cfg:%s]' % (self.name(), str(cfg)))

        log_level = cfg.get('log_level') or 'info'
        filename  = os.path.expandvars(cfg['path'])

        dirpath = os.path.split(filename)

        if dirpath[0] and not os.path.exists(dirpath[0]):
            raise xLoco('Invalid config, directory not found for [path] [provider:%s, path:%s]' % (self.name(), str(filename)))

        logging.basicConfig(level=getattr(logging, log_level.upper()))

        logger           = logging.getLogger(self.name())
        logger.propagate = False

        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(filename, 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT, self.TIMESTAMP_FORMAT))
        file_handler.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(file_handler)

        if cfg.get('stdout'):
            import sys

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(logging.Formatter(self.CONSOLE_FORMAT, self.TIMESTAMP_FORMAT))
            stream_handler.setLevel(getattr(logging, log_level.upper()))
            logger.addHandler(stream_handler)

        return logger
