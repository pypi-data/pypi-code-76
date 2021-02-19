#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 3.6
# @Filename:    companionsKQMLDispatcher.py
# @Author:      Samuel Hill
# @Date:        2020-09-11 07:48:36
# @Last Modified by:    Samuel Hill
# @Last Modified time:  2020-09-11 08:46:17

"""
General description of purpose.

More specific lorem ipsum dolor sit amet, consectetur adipiscing elit.
Quisque a lacus nulla. Vestibulum sodales eros ligula. Nullam euismod
libero magna.
"""

from logging import getLogger
from kqml import KQMLDispatcher, KQMLPerformative, KQMLException

LOGGER = getLogger(__name__)


class CompanionsKQMLDispatcher(KQMLDispatcher):
    """Dispatcher hookup to modify messages as they come in and to adjust
    logging.
    """

    def start(self):
        try:
            while True:
                msg = self.reader.read_performative()
                print(msg)
                msg_list = [remove_packaging(s) for s in msg.to_string.split()]
                KQMLPerformative.from_string(' '.join(msg_list))
                self.dispatch_message(msg)
        # This signal allows the dispatcher to stop blocking and return without
        # closing the connection to the socket and exiting
        except KQMLException:
            return
        except KeyboardInterrupt:
            LOGGER.warning('Keyboard interrupt received')
            self.receiver.receive_eof()
        except EOFError:
            LOGGER.debug('EOF received')
            self.receiver.receive_eof()
        except IOError as ex:
            if not self.shutdown_initiated:
                self.receiver.handle_exception(ex)
        except ValueError as err:
            LOGGER.error('Value error during reading')
            LOGGER.exception(err)
            return

    def shutdown(self):
        self.shutdown_initiated = True
        try:
            LOGGER.debug('KQML dispatcher shutting down')
            self.reader.close()
        except IOError:
            LOGGER.error('KQML dispatched IOError.')


def remove_packaging(symbol: str):
    """Remove package names from lisp such as common-lisp-user::

    Args:
        symbol (str): string to have package name striped

    Returns:
        str: symbol input with package name removed (if present)
    """
    split_symbol = symbol.split('::')
    return symbol if len(split_symbol) == 1 else split_symbol[1]
