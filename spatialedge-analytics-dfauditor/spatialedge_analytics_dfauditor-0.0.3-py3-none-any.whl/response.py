import numpy as np

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

    def __init__(self, size, lower_bound=0, upper_bound=1):
        self.type = 'HISTOGRAM'
        self.attr = None
        self.size = size
        self.bin_config = np.linspace(lower_bound, upper_bound, size + 1)
        self.__dict__.update(dict().fromkeys(
            ['bin_count_{}'.format(x) for x in range(0, size)]
        ))
        self.__dict__.update(dict().fromkeys(
            ['bin_range_{}'.format(x) for x in range(0, size)]
        ))


    def load(self, counts):
        """
        load the histogram bin values/counts into response object
        :param counts: a list of counts per bin
        :param bin_config: the bin configuration used to generate these bins
        :return:
        """
        if len(counts) != self.size:
            raise ValueError(f"Counts do not match number of bins {self.size}")

        for label, content in counts.reset_index().sort_values(by=['id', 'index'], ascending=[False, True]).items():
            if label == 'index':
                i = 0
                for inter in content:
                    bin_str = str(inter)

                    if inter.left <= self.bin_config[0]:
                        bin_str = bin_str.replace('(', '[')

                    self.__dict__['bin_range_{}'.format(i)] = bin_str
                    i = i + 1

            if label == 'id':
                i = 0
                for val in content:
                    self.__dict__['bin_count_{}'.format(i)] = val
                    i = i + 1

        del self.__dict__['bin_config']

