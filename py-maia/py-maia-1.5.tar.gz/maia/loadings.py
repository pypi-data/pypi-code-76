import time


def printr(text):
    print(text, end='\r')


class Loading:
    def __init__(self):
        pass

    @staticmethod
    def usual(xrange: dict):
        for i in xrange:
            if isinstance(i, int):
                yield str(i) + '%'
            raise ValueError

    @staticmethod
    def user_load(xrange: dict, desc='Object: %'):
        for x in xrange:
            try:
                yield desc.replace('%', x)
            except:
                raise ValueError
