import mxdevtool as mx


class Quote:
    def __init__(self, name, v):
        self.name = name
        self.v = v

    def toDict(self):
        return self.__dict__


class SimpleQuote(Quote):
    def __init__(self, name, v):
        Quote.__init__(self, name, v)


class FxRateQuote(Quote):
    def __init__(self, name, v):
        Quote.__init__(self, name, v)


class ForwardFxRateQuote(Quote):
    def __init__(self, name, v):
        Quote.__init__(self, name, v)


class InterestRateQuote(Quote):
    def __init__(self, name, v):
        Quote.__init__(self, name, v)