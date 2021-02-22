import unittest

import take_blipscore as tbs


class TestRun(unittest.TestCase):
    result = tbs.run(satisfaction_rate=0.67,
                     resolution_rate=0.82)
    
    def test_rate(self):
        """Check if the metric is calculated correctly."""
        expected = 0.7665976833542061
        actual = self.result["rate"]
        self.assertEqual(expected, actual)
        
    def test_return_type(self):
        """Check if return is type dict"""
        self.assertIsInstance(self.result, dict)
    
    def test_return_struct(self):
        """Check if return has default structure"""
        expected = ["rate", "operation"]
        actual = list(self.result.keys())
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
