__version__ = '0.3.0'
__title__ = 'koinput'
__author__ = 'k0per'
__copyright__ = 'Copyright 2021-present k0per'

from colorama import init

init()

from koinput.menu import Menu
from koinput.inputs import int_input, float_input
from koinput.progress_bar import ProgressBar

__all__ = [
    'int_input',
    'float_input',
    'Menu',
    'ProgressBar'
]
