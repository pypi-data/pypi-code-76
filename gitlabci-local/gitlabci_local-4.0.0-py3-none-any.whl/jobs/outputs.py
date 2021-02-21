#!/usr/bin/env python3

# Components
from ..prints.colors import Colors
from ..system.platform import Platform

# Outputs class
class Outputs:

    # Debugging
    @staticmethod
    def debugging(container_exec, container_name, shell):

        # Debugging informations
        print(' ')
        print(
            '  %s‣ INFORMATION: %sUse \'%s%s %s %s%s\' commands for debugging. Interrupt with Ctrl+C...%s'
            % (
                Colors.YELLOW,
                Colors.BOLD,
                Colors.CYAN,
                container_exec,
                container_name,
                shell,
                Colors.BOLD,
                Colors.RESET,
            ))
        print(' ')
        Platform.flush()

    # Interruption
    @staticmethod
    def interruption():

        # Interruption output
        print(' ')
        print(' ')
        print(
            '  %s‣ WARNING: %sUser interruption detected, stopping the container...%s' % (
                Colors.YELLOW,
                Colors.BOLD,
                Colors.RESET,
            ))
        print(' ')
        Platform.flush()

    # Warning
    @staticmethod
    def warning(message): # pragma: no cover

        # Warning output
        print('  %s‣ WARNING: %s%s%s' % (
            Colors.YELLOW,
            Colors.BOLD,
            message,
            Colors.RESET,
        ))
        print(' ')
        Platform.flush()
