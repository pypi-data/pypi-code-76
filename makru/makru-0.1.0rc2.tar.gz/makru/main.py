import sys
from .makru import Makru, Panic


def main():
    try:
        Makru().main()
    except Panic as e:
        print("panic: {}".format(e.message))
        sys.exit(1)


if __name__ == "__main__":
    main()
