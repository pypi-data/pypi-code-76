import unittest
import pandas as pd

import take_resolution as tr


class TestRun(unittest.TestCase):
    bot_identity = "bmgrouterprod@msging.net"
    start_date = "2020-06-01"
    end_date = "	2020-07-01"
    
    input_test = pd.DataFrame({"DAUs": [13487, 13859, 12979, 12342, 17030, 9631, 6099, 15574, 16031, 18303, 14510,
                                        14812, 8971, 6507, 15770, 17431, 17653, 15827, 15074, 10705, 7229, 16264,
                                        16047, 16837, 17628, 18583, 12989, 8626, 18384, 19437],
                               "amount": [11198, 11310, 11164, 10571, 11277, 7903, 4968, 11659, 12680, 14889, 11771,
                                          11570, 7719, 5795, 12383, 13676, 13882, 12467, 11822, 8701, 6171, 13065,
                                          12890, 13099, 14085, 15079, 10776, 6896, 15837, 15817]})
        
    result = tr.run(dataframe=input_test,
                    dau_column="DAUs",
                    amount="amount")

    def test_rate(self):
        """Check if the metric is calculated correctly."""
        expected = 0.803
        actual = round(self.result["rate"], 3)
        self.assertEqual(expected, actual)
    
    def test_daily_metric_return(self):
        """Check if daily metric is calculated as expected."""
        expected_list = [0.830281, 0.816076, 0.860159, 0.856506, 0.662184, 0.820579, 0.81456, 0.748619, 0.790968,
                         0.813473, 0.811234, 0.781123, 0.860439, 0.890579, 0.785225, 0.784579, 0.786382, 0.787705,
                         0.784264, 0.812798, 0.853645, 0.803308, 0.803265, 0.777989, 0.799013, 0.811441, 0.829625,
                         0.799444, 0.861456, 0.813757]
        
        expected = list(map(lambda x: round(x, 2), expected_list))
        actual = list(map(lambda x: round(x, 2), self.result["daily_resolution"]))
        self.assertEqual(expected, actual)
    
    def test_return_type(self):
        """Check if return is type dict"""
        self.assertIsInstance(self.result, dict)
    
    def test_return_struct(self):
        """Check if return has default structure"""
        expected = ["rate", "daily_resolution", "operation"]
        actual = list(self.result.keys())
        self.assertEqual(expected, actual)
        
    def test_dataframe_columns_independence(self):
        """Check if the project is bonded by the column name"""
        self.input_test.columns = ["a", "b"]
        result = tr.run(dataframe=self.input_test,
                        dau_column="a",
                        amount="b")
        expected = 0.803
        actual = round(result["rate"], 3)
        self.assertEqual(expected, actual)
    
    def test_dataframe_type(self):
        """Check if the amount raise TypeError for others types"""
        input_test = pd.DataFrame({"DAUs": [13487], "amount": [11198]})
        _ = tr.run(dataframe=input_test,
                   dau_column="DAUs",
                   amount="amount")

        with self.assertRaises(TypeError):
            tr.run(dataframe="testing",
                   dau_column="DAUs",
                   amount="amount")
            

if __name__ == '__main__':
    unittest.main()
