print("hello from snir's package 0.1.4")
from playsound import playsound

from sty import Style, RgbFg, Sgr
from sty import Style, RgbFg
from sty import fg


reset = '\033[0m'
fg.cyan = Style(RgbFg(0, 255, 255))
fg.red = Style(RgbFg(255, 0, 0))
fg.yellow = Style(RgbFg(255, 255, 0))
fg.green = Style(RgbFg(0, 255, 0))
fg.blue = Style(RgbFg(0, 70, 255))
bold_style = '\033[1m'
underline_style = '\033[4m'
def purple(txt):
    return '\033[95m' + str(txt) + reset


def header(txt):
    return '\033[93m' + str(txt) + reset


def bold(txt):
    return '\033[1m' + str(txt) + reset


def underline(txt):
    return '\033[4m' + str(txt) + reset


def blue(txt):
    return '\033[94m' + str(txt) + reset


def green(txt):
    return '\033[92m' + str(txt) + reset


def red(txt):
    return '\033[91m' + str(txt) + reset

def bright_red(txt):
    return fg.red + txt + reset

def black(txt):
    return '\u001b[30m' + str(txt) + reset


def cyan(txt):
    fg.cyan = Style(RgbFg(0, 255, 255))

    return fg.cyan + txt + reset


def error(txt):
    """identical to fail"""
    return fg.red + "\033[1m" + "\033[4m" + txt + reset


def fail(txt):
    """identical to error"""
    return fg.red + "\033[1m" + "\033[4m" + txt + reset


def bright_yellow(txt):
    return fg.yellow + txt + reset


def bright_green(txt):
    return fg.green + txt + reset


def bright_blue(txt):
    return fg.blue + txt + reset


def title(txt):
    return "\033[93m" + txt + reset

#todo __________________________________________________________________________________________________

def startup_sound():
    playsound("startup.wav", block=False)


def error_sound():
    playsound("negativebeep.wav", block=False)


def success_sound():
    playsound("success.wav", block=False)


def click_sound():
    playsound("first_click.wav", block=False)


def click_sound1():
    playsound("second_click.wav", block=False)



