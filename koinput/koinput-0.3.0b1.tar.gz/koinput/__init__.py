__version__ = '0.3.0b1'
__title__ = 'koinput'
__author__ = 'k0per'
__copyright__ = 'Copyright 2021-present k0per'

from koinput.menu import Menu
from koinput.inputs import int_input, float_input
from koinput.progress_bar import ProgressBar
from colorama import init

init()

__all__ = [
    'int_input',
    'float_input',
    'Menu',
    'ProgressBar'
]
