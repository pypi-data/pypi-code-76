"""Groups papers using the NIH percentile"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


class NihGrouper:
    """Groups papers using the NIH percentile"""

    def __init__(self, min1=2.1, min2=15.7, min3=83.9, min4=97.5):
        self.min1 = min1
        self.min2 = min2
        self.min3 = min3
        self.min4 = min4

    def get_group(self, nih_percentile):
        """Assign group numbers to the NIH percentile values using the 68-95-99.7 rule"""
        # No NIH percentile yet assigned. This paper should be checked out.
        if nih_percentile is None:
            return 5
        #  2.1% -3 SD: Very low citation rate
        if nih_percentile < self.min1:  # default: 2.1
            return 0
        # 13.6% -2 SD: Low citation rate
        if nih_percentile < self.min2:  # default: 15.7
            return 1
        # 68.2% -1 SD to +1 SD: Average citation rate
        if nih_percentile < self.min3:  # default: 83.9
            return 2
        # 13.6% +2 SD: High citation rate
        if nih_percentile < self.min4:  # default: 97.5
            return 3
        #  2.1% +3 SD: Very high citation rate
        return 4

    def add_arguments(self, parser):
        """Add NIH grouper arguments to the parser"""
        parser.add_argument(
            '-1', metavar='MIN1', dest='min1', default=self.min1, type=float,
            help='Minimum NIH percentile to be placed in group 1 (default: {D})'.format(D=self.min1))
        parser.add_argument(
            '-2', metavar='MIN2', dest='min2', default=self.min2, type=float,
            help='Minimum NIH percentile to be placed in group 2 (default: {D})'.format(D=self.min2))
        parser.add_argument(
            '-3', metavar='MIN3', dest='min3', default=self.min3, type=float,
            help='Minimum NIH percentile to be placed in group 3 (default: {D})'.format(D=self.min3))
        parser.add_argument(
            '-4', metavar='MIN4', dest='min4', default=self.min4, type=float,
            help='Minimum NIH percentile to be placed in group 4 (default: {D})'.format(D=self.min4))


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
