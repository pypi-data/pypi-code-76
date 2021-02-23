class StatsResponse(object):

    def __init__(self):
        self.__dict__.update(dict().fromkeys({'attr', 'type'}))


class Numeric(StatsResponse):

    def __init__(self):
        super(Numeric, self).__init__()
        self.__dict__.update(dict().fromkeys(
            {'mean', 'std', 'variance',
             'min', 'max', 'range', 'kurtosis', 'skewness',
             'mad', 'p_zeros', 'p_nan', 'median', 'iqr'
             }
        ))
        self.type = 'NUMERIC'


class String(StatsResponse):

    def __init__(self):
        super(String, self).__init__()
        self.__dict__.update(dict().fromkeys(
            {'distinct', 'freq'}
        ))
        self.type = 'STRING'
        self.freq = list()


class Bins(StatsResponse):

    def __init__(self, size):
        self.type = 'HISTOGRAM'
        self.attr = None
        self.size = size
        self.bins = []
        self.__dict__.update(dict().fromkeys(
            ['bin_count_{}'.format(x) for x in range(0, size)]
        ))

    def load(self, counts: list):
        """
        load the histogram bin values/counts into response object
        :param counts: a list of counts per bin
        :return:
        """
        if len(counts) != self.size:
            raise ValueError(f"Counts do not match number of bins {self.size}")
        for i, val in enumerate(counts):
            setattr(self, 'bin_count_{}'.format(i), val)
