""" Event Logging """

import shutil
import re
from termcolor import colored
from enum import IntEnum


red = lambda x: colored(x, 'red')
green = lambda x: colored(x, 'green')
yellow = lambda x: colored(x, 'yellow')

def expression(sstring):
    """ Convert a list expression into a string """
    def expr(sstring):
        out = "("
        for string in sstring:
            if isinstance(string, list):
                out += expr(string)
            else:
                out += str(string) + " "

        out += "\b) "
        return out

    return expr(sstring) + "\b"

def rendered(string):
    """ Get the string without terminal escape codes """
    regex = re.compile(r"\x1b\[[;\d]*[A-Za-z]", re.VERBOSE)
    return regex.sub("", string)

def width():
    """ Get width of terminal window """
    return shutil.get_terminal_size((80, 20)).columns

def padded(string, char):
    """ Wrap string with char
        Ex: padded("ola", "=") -> =========ola========
    """
    padding1 = char * ((width() - len(rendered(string))) // 2)
    padding2 = char * ((width() - len(rendered(string)) + 1) // 2)
    return padding1 + string + padding2

class Stats():
    """ Stats holder for tests """
    def __init__(self):
        self.pass_count = 0
        self.fail_count = 0
        self.assert_fail = 0
        self.assert_sucess = 0

    def passed(self):
        """Count passed test."""
        self.pass_count += 1

    def failed(self):
        """ Counte failed test."""
        self.fail_count += 1

    def total(self):
        """ Total count of tests."""
        return self.fail_count + self.pass_count

    def assert_failed(self):
        """Count assert failed."""
        self.assert_fail += 1

    def assert_passed(self):
        "Count assert passed."""
        self.assert_sucess += 1

class Level(IntEnum):
    DEBUG = 0
    ERROR = 1
    LOG = 2

class Logger():
    """ Log events """
    def __init__(self):
        self.repl = False
        self.test_count = 0
        self.level = Level.DEBUG
        self.stats = Stats()
        self._stop = False

    def start(self):
        print(padded(" test session starts ", "="))

    def stop(self):
        self._stop = True
        del self

    def set_repl(self):
        self.repl = True

    def set_level(self, level):
        self.level = level

    def print(self, level, string):
        if level >= self.level:
            print(string)

    def debug(self, s):
        self.print(Level.DEBUG, yellow("Debug: ") + s)

    def error(self, s):
        self.print(Level.ERROR, red("Error: ") + s)

    def log(self, s):
        self.print(Level.LOG, green("Log: ") + s)

    def launch(self, path):
        return

    def test(self, name, result):
        """ Output test result."""
        self.test_count += 1
        padding = " " * (width() - 2 - len(name) - 14)
        if result:
            self.stats.passed()
            self.print(Level.LOG, f"{name}: {green(' ✓')} {padding} [{self.test_count}]")
        else:
            self.stats.failed()
            self.print(Level.LOG, f"{name}: {red('❌')} {padding} [{self.test_count}]")


    def asserts(self, result, exps, evaled):
        """ Outputs assert result."""
        if result.is_err():
            return result
        result = result.ok()
        if not result:
            self.stats.assert_failed()
            self.print(Level.LOG, f"{red('Error')}: {expression(exps)} => {expression(evaled)} ❌")
        else:
            self.stats.assert_passed()


    def __del__(self):
        if self._stop:
            return
        if self.repl:
            return
        stats = ""
        if self.stats.pass_count == self.stats.total():
            stats = green(f" {self.stats.pass_count} passed ")
        else:
            stats = f" {red(f'{self.stats.fail_count} failed')},"
            stats += f"{green(f'{self.stats.pass_count} passed')} "
        print("")
        print(padded(stats, "="))


logger = Logger()
