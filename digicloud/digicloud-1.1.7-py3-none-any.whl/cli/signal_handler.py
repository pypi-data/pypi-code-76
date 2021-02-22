import sys


def interrupt_handler(sig, frame):
    print('\nOperation canceled')
    sys.exit(0)
