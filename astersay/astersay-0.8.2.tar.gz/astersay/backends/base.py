#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from logging import getLogger


class Listener:
    chunk_size = 4000
    # Максимальный размер потокового файла для Яндекса - 10 мегабайт.
    max_size = 10485760
    total_size = 0
    _continue = True
    logger = getLogger('astersay.backends.Listener')

    def __init__(self, stream):
        self._stream = stream

    def has_continue(self):
        return self._continue and (
            self.total_size + self.chunk_size < self.max_size)

    def listen(self):
        chunk_size = self.chunk_size
        stream_read = self._stream.read
        logger_debug = self.logger.debug
        logger_debug('stream: %s', self._stream)

        chunk_number = 0
        while self.has_continue():
            chunk_number += 1
            chunk = stream_read(chunk_size)
            length = len(chunk)
            # logger_debug('chunck %d length is %d', chunk_number, length)
            if length == 0:
                self.stop()
            self.total_size += length
            yield chunk
        logger_debug('listener ended, total size %d', self.total_size)

    def stop(self):
        self._continue = False
        self.logger.debug('listener stopped')


class BaseBackend:

    def __init__(self):
        cls = self.__class__
        name = '%s.%s' % (cls.__module__, cls.__name__)
        self.logger = getLogger(name)

    def __str__(self):
        return str(self.__class__)[8:-2]
