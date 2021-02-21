import math


# fyra räknesätten
def add(x, y):
    try:
        return x + y
    except ValueError:
        return"Can't calculate that"

def sub(x, y):
    try:
        return x - y
    except ValueError:
        return"Can't calculate that"

def div(x, y):
    try:
        return x / y
    except ValueError:
        return "Can't calculate that"

def multi(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return "Can't divide by 0"

# potenser
def sqrt(x):
    try:
        return math.sqrt(x)
    except ValueError:
        return "Can't calculate that"

def raised(x, y):
    try:
        return x**y
    except ValueError:
        return "Can't calculate that"

# triogometri
def pythaguras(x, y):
    try:
        return sqrt(raised(x, 2) + raised(y, 2))
    except ValueError:
        return"Can't calculate that"

# övrigt
def factorial(x):
    try:
        return math.factorial(x)
    except ValueError:
        return "Can't calculate that"