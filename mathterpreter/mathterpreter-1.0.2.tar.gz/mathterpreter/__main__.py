import sys
from mathterpreter.main import interpret


def main():
    if not sys.argv:
        return print("pass an argument to calculate")

    print(interpret("".join(sys.argv[1:]) or sys.stdin.read()))


if __name__ == '__main__':
    main()
