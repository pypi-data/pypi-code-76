"""Log formatter, part of the neatlog package

LICENSE
   MIT (https://mit-license.org/)

COPYRIGHT
   © 2020 Steffen Brinkmann <s-b@mailbox.org>
"""

import inspect
import logging
from datetime import datetime
from pathlib import PurePosixPath

# get information about where neatlog was imported from
imported_from_file = inspect.stack(0)[-1].filename
stem = PurePosixPath(imported_from_file).stem

# handler variables
stream_handler = None
file_handler = None


# set overall log level
logging.getLogger().setLevel(logging.DEBUG)


class NeatlogFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    black = "\x1b[30m"
    red = "\x1b[31m"
    red_bright = "\x1b[91;1m"
    red_dim = "\x1b[31;2m"
    green = "\x1b[32m"
    green_bright = "\x1b[32;1m"
    green_dim = "\x1b[32;2m"
    yellow = "\x1b[33m"
    yellow_bright = "\x1b[93;1m"
    yellow_dim = "\x1b[33;2m"
    blue = "\x1b[34m"
    blue_bright = "\x1b[34;1m"
    blue_dim = "\x1b[34;2m"
    magenta = "\x1b[35m"
    magenta_bright = "\x1b[35;1m"
    magenta_dim = "\x1b[35;2m"
    cyan = "\x1b[36m"
    cyan_bright = "\x1b[36;1m"
    cyan_dim = "\x1b[36;2m"
    white = "\x1b[37m"
    white_bright = "\x1b[37;1m"
    white_dim = "\x1b[37;2m"
    redyellow = "\x1b[91;43;1m"
    reset = "\x1b[0m"

    regex_ipv4 = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    regex_ipv6 = (
        r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|"
        r"^::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$|"
        r"^[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}$|"
        r"^[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}$|"
        r"^(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}$|"
        r"^(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}$|"
        r"^(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}$|"
        r"^(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}::[0-9a-fA-F]{1,4}$|"
        r"^(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}::$"
    )
    regex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex_url = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    regex_phone = (
        r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|"
        r"8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"
    )
    regex_currency = r"[\$€¥£]([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?"
    regex_number = r"[-+]?((\.[0-9]+|[0-9]+\.[0-9]+)([eE][-+]?[0-9]+)?|[0-9]+)"
    regex_hexcolor = r"#?([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})?"
    regex_date = (
        r"(\d\d(\d\d)?-\d\d?-\d\d?|"
        r"((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|"
        r"((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|"
        r"((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|"
        r"(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|"
        r"((16|[2468][048]|[3579][26])00)|00)))|"
        r"(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|"
        r"((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|"
        r"((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|"
        r"(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))))"
    )
    regex_time = (
        r"((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|"
        r"(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))"
    )
    regex_isodatetime = (
        r"(\d{4})(?:-([0]\d|[1][0-2]))(?:-([0-2]\d|[3][01]))(?:T([01]\d|2[0-3]))"
        r"(?::([0-5]\d))(?::([0-5]\d)(?:\.(\d{1,7}?)|)|)(Z|([+-])([01]\d|2[0-3])(?::([0-5]\d)))$"
    )
    regex_path = (
        r"(\.\/|\/[\w\/(\\ )(\\{)(\\})(\\<)(\\>)(\\[)(\])\.\-]+|"
        r"\.[\w\/(\\ )(\\{)(\\})(\\<)(\\>)(\\[)(\])\.\-]|[\w\/(\\ )(\\{)(\\})(\\<)(\\>)(\\[)(\])\.\-]+\/)"
        r"([\w\/(\\ )(\\{)(\\})(\\<)(\\>)(\\[)(\])\.\-])*"
    )
    regex_string = r"(\"[^\"]+\"|\"\"\"[^\"]+\"\"\"|'[^']+'|'''[^']+''')"
    regex_backticks = r"(`[^`]+`|``[^`]+``)"

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style="%",
        prefix="",
        sep=" | ",
        suffix="",
        color=True,
        compact=False,
    ):

        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

        if fmt is not None:
            self.fmt = (
                fmt.replace("%(funcName)", "%(_funcName)")
                .replace("%(lineno)", "%(_lineno)")
                .replace("%(filename)", "%(_filename)")
            )
        else:
            self.fmt = ""
            if prefix:
                self.fmt += f"{prefix}"

            if compact:
                levelname_width = 1
                sep = sep.strip()
            else:
                levelname_width = 8
            self.fmt += (
                f"%(asctime)s{sep}{stem}{sep}%(_filename)s:%(_lineno)-4d{sep}%(_funcName)s{sep}"
                f"%(levelname)-{levelname_width}s{sep}%(message)s"
            )

            if suffix:
                self.fmt += f"{suffix}"

        self.format_colors = {
            logging.DEBUG: self.cyan_bright,
            logging.INFO: self.green_bright,
            logging.WARNING: self.yellow_bright,
            logging.ERROR: self.red_bright,
            logging.CRITICAL: self.redyellow,
        }

        self.formats = {
            logging.DEBUG: self.fmt,
            logging.INFO: self.fmt,
            logging.WARNING: self.fmt,
            logging.ERROR: self.fmt,
            logging.CRITICAL: self.fmt,
        }

        if color:
            for lev in self.formats:
                i = self.formats[lev].find("%(levelname)")
                j = self.formats[lev].find("s", i) + 1
                self.formats[lev] = (
                    self.formats[lev][:i]
                    + self.format_colors[lev]
                    + self.formats[lev][i:j]
                    + self.reset
                    + self.formats[lev][j:]
                )

    def format(self, record):
        if not hasattr(record, "_funcName"):
            record._funcName = record.funcName
        if not hasattr(record, "_filename"):
            record._filename = record.filename
        if not hasattr(record, "_lineno"):
            record._lineno = record.lineno

        _log_fmt = self.white_dim + self.formats.get(record.levelno)
        formatter = logging.Formatter(_log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# TODO: make logging level configurable for files and streams separately
def set_log_level(lev: int):
    for handler in logging.getLogger().handlers:
        handler.setLevel(lev)


# TODO: off several default values for fmt
# '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
def config_logger(
    log_to_stream=None,
    log_to_file=None,
    level=logging.WARNING,
    compact=False,
    prefix="",
    sep=" | ",
    suffix="",
    fmt=None,
    datefmt=None,
    style="%",
    stream=None,
    color=True,
    filename=None,
    mode="a",
    encoding=None,
    delay=False,
):
    """Configure and switch on or off the logging handlers.
    For log_to_stream and log_to_stream, None means "do nothing", True means "switch on and configure",
    False means "switch off"."""

    global stream_handler
    global file_handler

    logger = logging.getLogger()
    if log_to_stream is not None:
        logger.removeHandler(stream_handler)
        if log_to_stream:
            stream_handler = logging.StreamHandler(stream)
            stream_handler.setLevel(level)
            stream_handler.setFormatter(
                NeatlogFormatter(
                    fmt=fmt,
                    datefmt=datefmt,
                    style=style,
                    prefix=prefix,
                    sep=sep,
                    suffix=suffix,
                    color=color,
                    compact=compact,
                )
            )
            logger.addHandler(stream_handler)
        else:
            stream_handler = None

    if log_to_file is not None:
        logger.removeHandler(file_handler)
        if log_to_file:
            _timestamp = datetime.now().isoformat(timespec="seconds")
            _filename = filename or f"log_{_timestamp}.log"
            file_handler = logging.FileHandler(
                _filename, mode=mode, encoding=encoding, delay=delay
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(
                NeatlogFormatter(
                    fmt=fmt,
                    datefmt=datefmt,
                    style=style,
                    prefix=prefix,
                    sep=sep,
                    suffix=suffix,
                    color=False,
                    compact=compact,
                )
            )
            logger.addHandler(file_handler)
        else:
            file_handler = None

    if compact:
        logging.addLevelName(logging.DEBUG, "D")
        logging.addLevelName(logging.INFO, "I")
        logging.addLevelName(logging.WARNING, "W")
        logging.addLevelName(logging.ERROR, "E")
        logging.addLevelName(logging.CRITICAL, "C")
    else:
        logging.addLevelName(logging.DEBUG, "DEBUG")
        logging.addLevelName(logging.INFO, "INFO")
        logging.addLevelName(logging.WARNING, "WARNING")
        logging.addLevelName(logging.ERROR, "ERROR")
        logging.addLevelName(logging.CRITICAL, "CRITICAL")


# def log(level, msg, filename, lineno, funcName):
#     logging.log(level, msg)


# default configuration
config_logger(log_to_stream=True, log_to_file=False)

# adjust third party logging
matplotlib_logger = logging.getLogger("matplotlib")
matplotlib_logger.setLevel(level=logging.WARNING)
flake8_logger = logging.getLogger("flake8")
flake8_logger.setLevel(level=logging.ERROR)
filelock_logger = logging.getLogger("filelock")
filelock_logger.setLevel(level=logging.ERROR)
pillow_logger = logging.getLogger("PIL.PngImagePlugin")
pillow_logger.setLevel(level=logging.ERROR)
