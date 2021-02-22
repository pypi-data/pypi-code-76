import unittest

from satisfaction_config import Config


class TestConfig(unittest.TestCase):
    def test_KNOWN_MANUAL_INPUTS(self):
        """Test if SATISFACTION_WEIGHT can be called from satisfaction_config and if has default value."""
        self.assertIsInstance(Config.KNOWN_MANUAL_INPUTS, list)
    
    def test_SCALE_TRANSLATIONS(self):
        """Test if RESOLUTION_WEIGHT can be called from satisfaction_config and if has default value."""
        self.assertIsInstance(Config.SCALE_TRANSLATIONS, list)


if __name__ == '__main__':
    unittest.main()
