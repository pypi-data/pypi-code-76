import unittest
import pandas as pd

import take_satisfaction as ts


class TestRun(unittest.TestCase):
    bot_identity = "centaurobc@msging.net"
    start_date = "2020-06-01"
    end_date = "	2020-07-01"
    
    pdf = pd.DataFrame(
        {"Action": ["Pessimo", "Excelente", "Otimo", "Ok", "Ruim"],
         "amount": [173, 57, 114, 168, 58]})
    
    result = ts.run(dataframe=pdf,
                    scale_column="Action",
                    amount_column="amount",
                    similarity_threshold=80)
    
    def test_run_rate(self):
        """Check if rate is calculated as expected."""
        expected = 0.42280701754385963
        actual = self.result["rate"]
        self.assertEqual(expected, actual)

    def test_run_default_similarity_threshold(self):
        """Check if rate is calculated as expected."""
        expected = 80
        actual = self.result["similarity_threshold"]
        self.assertEqual(expected, actual)
        
    def test_return_type(self):
        """Check if return is type dict"""
        self.assertIsInstance(self.result, dict)
    
    def test_return_struct(self):
        """Check if return has default structure"""
        expected = ["rate", "similarity_threshold", "operation"]
        actual = list(self.result.keys())
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
