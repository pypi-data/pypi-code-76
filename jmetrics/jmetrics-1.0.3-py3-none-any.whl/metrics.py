import re
from numbers import Number


class Byte(int):
    """
    Memory value as byte

    >>> Byte(0)
    0
    >>> Byte(2)
    2
    >>> Byte('65')
    65
    >>> Byte('89B')
    89
    >>> Byte('1k')
    1000
    >>> Byte('1ki')
    1024
    >>> Byte('1.5k')
    1500
    >>> Byte('1.5ki')
    1536
    >>> Byte('1ki') + Byte('-1k')
    24
    >>> str(Byte(0))
    '0'
    >>> str(Byte('70M'))
    '70MB'
    >>> str(Byte('43Mi'))
    '43MiB'
    >>> str(Byte('1.5M'))
    '1500kB'
    """

    __sizes = {
        'Ti': 1 << 40,
        'T': 1000 ** 4,
        'Gi': 1 << 30,
        'G': 1000 ** 3,
        'Mi': 1 << 20,
        'M': 1000 ** 2,
        'ki': 1 << 10,
        'k': 1000 ** 1,
        '':  1,
    }

    __re = re.compile(r"""^
        (?P<float>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)  # The number as float
        (?P<unit>k|M|G|T|ki|Mi|Gi|Ti)?[Bo]?                 # The unit
    $""", re.VERBOSE)

    def __new__(cls, x=0):
        if isinstance(x, Number):
            return super().__new__(cls, x)

        match = cls.__re.match(x)
        if not match:
            raise ValueError("Not a valid byte representation")
        return super().__new__(cls, float(match.group('float')) * cls.__sizes[match.group('unit') or ''])

    def __str__(self):
        if not self:
            return "0"
        for unit, size in type(self).__sizes.items():
            d, m = divmod(self, size)
            if not m:
                return f"{d}{unit}B"
        return super().__str__()


class Time(int):
    """
    Time value as second

    >>> Time(0)
    0
    >>> Time(2)
    2
    >>> Time('34')
    34
    >>> Time('43s')
    43
    >>> Time('12m')
    720
    >>> Time('1.5m')
    90
    >>> Time('3h')
    10800
    >>> Time('1d')
    86400
    >>> Time('2d3h12m43s')
    184363
    >>> str(Time(0))
    '0'
    >>> str(Time(12))
    '12s'
    >>> str(Time('59s'))
    '59s'
    >>> str(Time('12m'))
    '12m'
    >>> str(Time('1.5m'))
    '1m30s'
    >>> str(Time('8h'))
    '8h'
    >>> str(Time('9h02m'))
    '9h2m'
    >>> str(Time('4h20m10s'))
    '4h20m10s'
    >>> str(Time('2d3h12m43s'))
    '2d3h12m43s'
    """

    __re = re.compile(r"""^(
        (?P<second1>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)s?  # only seconds as float
        |(?P<minute1>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)m  # or minutes as float..
        ((?P<second2>[0-6]?[0-9])s)?                            # .. with optionnal seconds in base 60
        |(?P<hour1>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)h    # or hours as float..
        ((?P<minute2>[0-6]?[0-9])m)?                            # .. with optionnal minutes in base 60..
        ((?P<second3>[0-6]?[0-9])s)?                            # .. and optionnal seconds in base 60
        |(?P<day1>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)d     # or days as float..
        ((?P<hour2>2[0-4]|[01]?[0-9])h)?                        # .. with optionnal hours in base 24..
        ((?P<minute3>[0-6]?[0-9])m)?                            # .. and optionnal minutes in base 60..
        ((?P<second4>[0-6]?[0-9])s)?                            # .. and optionnal seconds in base 60
    )$""", re.VERBOSE)

    def __new__(cls, x=0):
        if isinstance(x, Number):
            return super().__new__(cls, x)

        match = cls.__re.match(x)
        if not match:
            raise ValueError("Not a valid time representation")

        s1 = float(match.group('second1') or 0)
        s2 = float(match.group('second2') or 0)
        s3 = float(match.group('second3') or 0)
        s4 = float(match.group('second4') or 0)
        m1 = float(match.group('minute1') or 0) * 60
        m2 = float(match.group('minute2') or 0) * 60
        m3 = float(match.group('minute3') or 0) * 60
        h1 = float(match.group('hour1') or 0) * 60 * 60
        h2 = float(match.group('hour2') or 0) * 60 * 60
        d1 = float(match.group('day1') or 0) * 60 * 60 * 24
        return super().__new__(cls, d1 + h1 + h2 + m1 + m2 + m3 + s1 + s2 + s3 + s4)

    def __str__(self):
        if not self:
            return "0"
        s = ""
        for rank, unit in ((60 * 60 * 24, 'd'), (60 * 60, 'h'), (60, 'm'), (1, 's')):
            div, mod = divmod(self, rank)
            if div:
                s += f"{div}{unit}"
                self = mod
        return s


if __name__ == '__main__':
    import sys
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
