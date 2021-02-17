import unittest
import pandas as pd
import cufflinks as cf
from commodplot import commodplottrace as cptr
from commodutil import transforms


class TestCommodPlotTrace(unittest.TestCase):

    def test_min_max_range(self):
        df = cf.datagen.lines(1, 5000)
        dft = transforms.seasonailse(df)
        res = cptr.min_max_range(dft, shaded_range=5)
        self.assertTrue(isinstance(res[0], pd.DataFrame))
        self.assertTrue(isinstance(res[1], int))


if __name__ == '__main__':
    unittest.main()


