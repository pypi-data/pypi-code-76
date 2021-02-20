def test_function():
    print('Hello world! The package appears to be working.')


class FunClass:
    def __init__(self, name=None, number=None):
        self.name = name
        self.number = number

    def multiplier(self, factor):
        return f'{self.name} multiplied by {factor} is {self.number * factor}!'


def concatenator(str1, str2):
    return str1+str2
