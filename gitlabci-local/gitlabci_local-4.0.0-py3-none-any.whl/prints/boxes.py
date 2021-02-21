#!/usr/bin/env python3

# Standard libraries
from shutil import get_terminal_size

# Components
from ..system.platform import Platform
from ..types.strings import Strings
from .colors import Colors

# Boxes class
class Boxes:

    # Constants
    __TOP_LEFT = '╭'
    __TOP_LINE = '─'
    __TOP_RIGHT = '╮'
    __MIDDLE_LEFT = '│'
    __MIDDLE_RIGHT = '│'
    __BOTTOM_LEFT = '╰'
    __BOTTOM_LINE = '─'
    __BOTTOM_RIGHT = '╯'
    __OFFSET_LINE = 2
    __PADDING_LINE = 2

    # Members
    __lines = None

    # Constructor
    def __init__(self):
        self.__lines = []

    # Adder
    def add(self, line):
        self.__lines += [line]

    # Printer
    def print(self):

        # Evaluate lines length
        length = max(len(Strings.strip(line)) for line in self.__lines)

        # Acquire terminal width
        columns, unused_rows = get_terminal_size()

        # Limit line length
        limit = columns - Boxes.__OFFSET_LINE - len(
            Boxes.__MIDDLE_LEFT) - 2 * Boxes.__PADDING_LINE - len(Boxes.__MIDDLE_RIGHT)
        if limit < 1: # pragma: no cover
            limit = 1
        if length > limit:
            length = limit

        # Header
        print(' ')

        # Print header line
        print('%s%s%s%s%s' %
              (' ' * Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__TOP_LEFT,
               Boxes.__TOP_LINE * (length + 2 * Boxes.__PADDING_LINE), Boxes.__TOP_RIGHT))

        # Print content lines
        for line in self.__lines:
            for part in Strings.wrap(line, length=length):
                print('%s%s%s%s%s%s%s%s' %
                      (' ' * Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__MIDDLE_LEFT,
                       ' ' * Boxes.__PADDING_LINE, Strings.center(part, length),
                       ' ' * Boxes.__PADDING_LINE, Colors.YELLOW, Boxes.__MIDDLE_RIGHT))

        # Print bottom line
        print('%s%s%s%s%s%s' %
              (' ' * Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__BOTTOM_LEFT,
               Boxes.__BOTTOM_LINE *
               (length + 2 * Boxes.__PADDING_LINE), Boxes.__BOTTOM_RIGHT, Colors.RESET))

        # Footer
        print(' ')
        Platform.flush()
