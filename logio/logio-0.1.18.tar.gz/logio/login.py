# -*- coding: utf-8 -*-
import os
import io
from io import open
import time
import codecs
import datetime
import threading
import logging
from tail import TailReader

logger = logging.getLogger(__name__)

def get_stdin_reader(encoding=None):
    if hasattr(os.sys.stdin, "reconfigure"):
        os.sys.stdin.reconfigure(encoding=encoding)
        return os.sys.stdin
    else:
        os.sys.stdin = codecs.getreader(encoding)(os.sys.stdin)
        return os.sys.stdin


LOG_INPUT_TYPES = {}

def register_input_type(name, klass):
    LOG_INPUT_TYPES[name] = klass

def unregister_input_type(name):
    del LOG_INPUT_TYPES[name]

def get_input_class(name):
    return LOG_INPUT_TYPES.get(name, None)

class LogInput(object):

    def __init__(self, settings):
        self.settings = settings or {}
        self.parser = None
        self.output = None
        self.filters = None
        # properties
        self.ignore_blank_lines = self.settings.get("ignore-blank-lines", True)
        self.encoding = self.settings.get("encoding", "utf-8")
        self.report_interval = self.settings.get("report-interval", 1)
        # private properties
        self.lines_handlered = 0
        self.last_reported_timestamp = time.time()
        # self.report_thread = threading.Thread(target=self.report)
        # self.report_thread.setDaemon(True)
        # self.report_thread.start()

    def set_handler(self, output, filters=None, parser=None):
        self.parser = parser
        self.output = output
        self.filters = filters

    def loop(self):
        raise NotImplementedError()

    def report(self):
        while True:
            time.sleep(self.report_interval)
            msg = "{0} lines handlered.".format(self.lines_handlered)
            logger.info(msg)

    def line_handler(self, line):
        self.lines_handlered += 1
        if self.filters:
            for filter in self.filters:
                if filter.line_filter(line) == False:
                    return
        if self.parser:
            line_info = self.parser.line_handler(line)
        else:
            line_info = {
                "_line": line,
            }
        return self.output.update(line_info)
    
    def flush_output(self):
        return self.output.flush()

    @classmethod
    def init(cls, settings):
        input_type = settings.get("type", "stdin")
        input_class = get_input_class(input_type)
        if not input_class:
            return None
        return input_class(settings)

class StdinInput(LogInput):

    def loop(self):
        reader = get_stdin_reader(self.encoding)
        for line in reader.readlines():
            line = line.rstrip(u"\r\n")
            if line or not self.ignore_blank_lines:
                self.line_handler(line)

class FileInput(LogInput):

    def __init__(self, settings):
        super().__init__(settings)
        # properties
        self.filename = self.settings["filename"]

    def loop(self):
        if self.filename:
            reader = io.open(self.filename, encoding=self.encoding)
        else:
            reader = get_stdin_reader(encoding=self.encoding)
        for line in reader.readlines():
            line = line.rstrip(u"\r\n")
            if line or not self.ignore_blank_lines:
                self.line_handler(line)

class TailInput(LogInput):

    def __init__(self, settings):
        super().__init__(settings)
        # properties
        self.filename = self.settings["filename"]
        self.offset_file = self.settings.get("offset-file", None)
        self.read_from_end = self.settings.get("read-from-end", False)
        self.backup_patterns = self.settings.get("backup-patterns", None)
        self.sleep_interval = self.settings.get("sleep-interval", 1)
        self.blocking = self._get_blockeding_setting()

    def _get_blockeding_setting(self):
        result = None
        if "non-blocking" in self.settings:
            result = not self.settings["non-blocking"]
        if "blocking" in self.settings:
            result = self.settings["blocking"]
        if result is None:
            result = True
        return result

    def loop(self):
        filereader = TailReader(
            self.filename,
            self.offset_file,
            self.read_from_end,
            self.encoding,
            self.backup_patterns,
            )
        while True:
            c = 0
            for line in filereader.readlines():
                line = line.rstrip(u"\r\n")
                if line or not self.ignore_blank_lines:
                    stored = self.line_handler(line)
                    c += 1
                    if stored:
                        filereader.update_offset()
            stored = self.flush_output()
            if stored:
                filereader.update_offset()
            if not self.blocking:
                break
            if c < 1:
                time.sleep(self.sleep_interval)


register_input_type("stdin", StdinInput)
register_input_type("file", FileInput)
register_input_type("tail", TailInput)
