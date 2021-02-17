import sys
from colorama import Fore


def int_input(input_suggestion='', greater=float('-inf'), less=float('inf'), console_style=Fore.RESET,
              error_message='Invalid number format.\n', error_message_style=Fore.RED,
              input_is_greater_than_less_error="The number is greater than acceptable.\n",
              input_is_less_than_greater_error="The number is less than acceptable.\n",
              input_is_less_error_style=None, input_is_greater_error_style=None,
              strictly_greater=True, strictly_less=True, input_suggestion_style=None) -> int:
    # type check
    if type(input_suggestion) != str:
        raise TypeError('input_suggestion must be str')
    if type(greater) != int and type(greater) != float:
        raise TypeError('greater must be int or float')
    if type(less) != int and type(less) != float:
        raise TypeError('greater must be int or float')
    if type(error_message) != str:
        raise TypeError('error_message must be str')
    if type(console_style) != str:
        raise TypeError('console_colour must be str')
    if type(error_message_style) != str:
        raise TypeError('error_message_colour must be str')
    if type(input_is_greater_than_less_error) != str:
        raise TypeError('input_is_greater_than_less_error must be str')
    if type(input_is_less_than_greater_error) != str:
        raise TypeError('input_is_less_than_greater_error must be str')
    if type(input_is_less_error_style) != str and input_is_less_error_style is not None:
        raise TypeError('input_is_greater_error_style must be str')
    if type(input_is_greater_error_style) != str and input_is_greater_error_style is not None:
        raise TypeError('input_is_greater_error_style must be str')
    if type(input_suggestion_style) != str and input_suggestion_style is not None:
        raise TypeError('input_suggestion_style must be str')
    if type(strictly_greater) != bool:
        raise TypeError('strictly_greater must be bool')
    if type(strictly_less) != bool:
        raise TypeError('strictly_less must be bool')

    # error colour
    if input_is_less_error_style is None:
        input_is_less_error_style = error_message_style
    if input_is_greater_error_style is None:
        input_is_greater_error_style = error_message_style

    # input
    while True:
        try:
            if input_suggestion_style is not None:
                sys.stdout.write(input_suggestion_style + '\r')
                sys.stdout.write(' ' * len(input_suggestion_style) + '\r')
                sys.stdout.write(input_suggestion + console_style)
            else:
                sys.stdout.write(input_suggestion)
            introduced = int(input().split()[0])
            if introduced <= greater and strictly_greater:
                sys.stdout.write(input_is_greater_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_greater_error_style) + '\r')
                sys.stdout.write(input_is_less_than_greater_error + console_style)
            elif introduced < greater and not strictly_greater:
                sys.stdout.write(input_is_greater_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_greater_error_style) + '\r')
                sys.stdout.write(input_is_less_than_greater_error + console_style)
            elif introduced >= less and strictly_less:
                sys.stdout.write(input_is_less_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_less_error_style) + '\r')
                sys.stdout.write(input_is_greater_than_less_error + console_style)
            elif introduced > less and not strictly_less:
                sys.stdout.write(input_is_less_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_less_error_style) + '\r')
                sys.stdout.write(input_is_greater_than_less_error + console_style)
            else:
                return introduced
        except Exception:
            sys.stdout.write(error_message_style + '\r')
            sys.stdout.write(' ' * len(error_message_style) + '\r')
            sys.stdout.write(error_message + console_style)


def float_input(input_suggestion='', greater=float('-inf'), less=float('inf'), console_style=Fore.RESET,
                error_message='Invalid number format.\n', error_message_style=Fore.RED,
                input_is_greater_than_less_error="The number is greater than acceptable.\n",
                input_is_less_than_greater_error="The number is less than acceptable.\n",
                input_is_less_error_style=None, input_is_greater_error_style=None,
                strictly_greater=True, strictly_less=True, input_suggestion_style=None) -> float:
    # type check
    if type(input_suggestion) != str:
        raise TypeError('input_suggestion must be str')
    if type(greater) != int and type(greater) != float:
        raise TypeError('greater must be int or float')
    if type(less) != int and type(less) != float:
        raise TypeError('greater must be int or float')
    if type(error_message) != str:
        raise TypeError('error_message must be str')
    if type(console_style) != str:
        raise TypeError('console_colour must be str')
    if type(error_message_style) != str:
        raise TypeError('error_message_colour must be str')
    if type(input_is_greater_than_less_error) != str:
        raise TypeError('input_is_greater_than_less_error must be str')
    if type(input_is_less_than_greater_error) != str:
        raise TypeError('input_is_less_than_greater_error must be str')
    if type(input_is_less_error_style) != str and input_is_less_error_style is not None:
        raise TypeError('input_is_greater_error_style must be str')
    if type(input_is_greater_error_style) != str and input_is_greater_error_style is not None:
        raise TypeError('input_is_greater_error_style must be str')
    if type(input_suggestion_style) != str and input_suggestion_style is not None:
        raise TypeError('input_suggestion_style must be str')
    if type(strictly_greater) != bool:
        raise TypeError('strictly_greater must be bool')
    if type(strictly_less) != bool:
        raise TypeError('strictly_less must be bool')

    # error colour
    if input_is_less_error_style is None:
        input_is_less_error_style = error_message_style
    if input_is_greater_error_style is None:
        input_is_greater_error_style = error_message_style

    # input
    while True:
        try:
            if input_suggestion_style is not None:
                sys.stdout.write(input_suggestion_style + '\r')
                sys.stdout.write(' ' * len(input_suggestion_style) + '\r')
                sys.stdout.write(input_suggestion + console_style)
            else:
                sys.stdout.write(input_suggestion)
            introduced = float(input().split()[0])
            if introduced <= greater and strictly_greater:
                sys.stdout.write(input_is_greater_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_greater_error_style) + '\r')
                sys.stdout.write(input_is_less_than_greater_error + console_style)
            elif introduced < greater and not strictly_greater:
                sys.stdout.write(input_is_greater_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_greater_error_style) + '\r')
                sys.stdout.write(input_is_less_than_greater_error + console_style)
            elif introduced >= less and strictly_less:
                sys.stdout.write(input_is_less_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_less_error_style) + '\r')
                sys.stdout.write(input_is_greater_than_less_error + console_style)
            elif introduced > less and not strictly_less:
                sys.stdout.write(input_is_less_error_style + '\r')
                sys.stdout.write(' ' * len(input_is_less_error_style) + '\r')
                sys.stdout.write(input_is_greater_than_less_error + console_style)
            else:
                return introduced
        except Exception:
            sys.stdout.write(error_message_style + '\r')
            sys.stdout.write(' ' * len(error_message_style) + '\r')
            sys.stdout.write(error_message + console_style)
