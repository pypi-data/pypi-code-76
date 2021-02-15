import typing
import functools
import platform
import logging
import os
import subprocess
import enum
from PyQt5 import QtGui


testing_bool = False

"""
class TestingEnum(enum.Enum):
    not_set = enum.auto()
    testing = enum.auto()
    production = enum.auto()


class TestingClass:
    testing_enum = TestingEnum.not_set

    @classmethod
    def get_testing_enum(cls) -> TestingEnum:
        return cls.testing_enum

    @classmethod
    def set_testing_enum(cls, i_testing) -> None:
        cls.testing_enum = i_testing
"""


VERSION_STR = '1.0.0-alpha27'
APPLICATION_NAME_STR = 'file-player'
SHORT_DESCRIPTION_STR = "A music player using the file system to order/structure files (rather than audio tags)"
APPLICATION_WEBSITE_STR = "https://gitlab.com/SunyataZero/file-player"
AUTHOR_NAME_STR = "Tord Dellsén (SunyataZero)"
# PYQT MIN VERSION

XPM_ICON_DATA = [
    "24 24 36 1", " 	c None",
    ".	c #0A8B0A", "+	c #077707", "@	c #045A04", "#	c #045D04",
    "$	c #098409", "%	c #056805", "&	c #087F08", "*	c #056705",
    "=	c #000000", "-	c #001A00", ";	c #088008", ">	c #0A8A0A",
    ",	c #013001", "'	c #034E03", ")	c #035203", "!	c #034A03",
    "~	c #066D06", "{	c #045804", "]	c #034B03", "^	c #045904",
    "/	c #024002", "(	c #098709", "_	c #024302", ":	c #035303",
    "<	c #045B04", "[	c #012C01", "}	c #001000", "|	c #000700",
    "1	c #087B08", "2	c #077607", "3	c #013101", "4	c #077507",
    "5	c #087E08", "6	c #066E06", "7	c #087A08",
    "       .........        ",
    "    ...............    ",
    "   .................   ",
    "  ...................  ",
    " .....................  ",
    " ...................... ",
    " +@@@@@@@#..$@@@@@#%&.. ",
    ".*=======-..;========@>.",
    ".*==,'''')..;===@@!===~.",
    ".*=={.......;===...@==].",
    ".*==^.......;===...~==/.",
    ".*=======@..;===..(_==:.",
    ".*=======<..;===[[}==|1.",
    ".*==!2222&..;=======34..",
    ".*=={.......;===22+;....",
    ".*=={.......;===........",
    ".*=={.......;===........",
    ".*=={.......;===........",
    ".5667.......(66~........",
    " ...................... ",
    "  ....................  ",
    "   ..................   ",
    "    ................    ",
    "      ............      "
]


def get_appl_path(*args) -> str:
    application_dir_str = os.path.dirname(__file__)
    full_path_str = application_dir_str
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def get_project_path(*args) -> str:
    application_dir_str = os.path.dirname(__file__)
    project_dir_str = os.path.dirname(application_dir_str)
    full_path_str = project_dir_str
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def debug_dr(func: typing.Callable):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        logging.debug(f"=== {func.__name__} was called")
        """
        logging.debug(f"{func.__code__.co_argcount=}")
        sig = inspect.signature(func)
        params = sig.parameters
        logging.debug(f"{sig.parameters=}")
        """
        func_arg_count_int = func.__code__.co_argcount
        func_name_str = func.__name__
        logging.debug(f"{func_name_str=}")
        if len(args) + 1 > func_arg_count_int and "clicked" in func_name_str:
            args = args[:-1]
        ret_val = func(*args, **kwargs)
        logging.debug(f"=== {func.__name__} returned {ret_val!r}")
        return ret_val
    return wrapper_func


def open_fd(i_fd_path: str):
    system_str = platform.system()
    if system_str == "Windows":
        os.startfile(i_fd_path)
    elif system_str == "Darwin":
        subprocess.Popen(["open", i_fd_path])
    else:
        subprocess.Popen(["xdg-open", i_fd_path])


class PaletteTypeEnum(enum.Enum):
    from_desktop_env = enum.auto()
    light = enum.auto()
    dark = enum.auto()


def get_palette(i_palette_type: PaletteTypeEnum) -> QtGui.QPalette:
        green_qcolor = QtGui.QColor(0, 128, 0)
        darkgray_qcolor = QtGui.QColor(64, 64, 64)
        black_qcolor = QtGui.QColor(32, 32, 32)
        white_qcolor = QtGui.QColor(250, 250, 250)
        yellow_qcolor = QtGui.QColor(200, 200, 0)
        almostblack_qcolor = QtGui.QColor(32, 32, 32)

        if i_palette_type == PaletteTypeEnum.light:
            light_qp = QtGui.QPalette()
            light_qp.setColor(QtGui.QPalette.Highlight, green_qcolor)
            light_qp.setColor(QtGui.QPalette.Link, green_qcolor)

            return light_qp
        elif i_palette_type == PaletteTypeEnum.dark:
            dark_qp = QtGui.QPalette()
            dark_qp.setColor(QtGui.QPalette.Window, darkgray_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Background, )
            dark_qp.setColor(QtGui.QPalette.WindowText, white_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Foreground, )
            dark_qp.setColor(QtGui.QPalette.Base, black_qcolor)
            dark_qp.setColor(QtGui.QPalette.AlternateBase, darkgray_qcolor)
            dark_qp.setColor(QtGui.QPalette.ToolTipBase, black_qcolor)
            dark_qp.setColor(QtGui.QPalette.ToolTipText, white_qcolor)
            # dark_qp.setColor(QtGui.QPalette.PlaceholderText, )
            dark_qp.setColor(QtGui.QPalette.Text, white_qcolor)
            dark_qp.setColor(QtGui.QPalette.Button, darkgray_qcolor)
            dark_qp.setColor(QtGui.QPalette.ButtonText, white_qcolor)
            dark_qp.setColor(QtGui.QPalette.BrightText, yellow_qcolor)

            # dark_qp.setColor(QtGui.QPalette.Light, green_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Midlight, green_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Dark, green_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Mid, green_qcolor)
            # dark_qp.setColor(QtGui.QPalette.Shadow, green_qcolor)

            dark_qp.setColor(QtGui.QPalette.Highlight, green_qcolor)
            dark_qp.setColor(QtGui.QPalette.HighlightedText, yellow_qcolor)
            dark_qp.setColor(QtGui.QPalette.Link, green_qcolor)
            dark_qp.setColor(QtGui.QPalette.LinkVisited, green_qcolor)
            # QtGui.QGuiApplication.setPalette(dark_qp)

            return dark_qp

        elif i_palette_type == PaletteTypeEnum.from_desktop_env:
            pass
        else:
            pass
