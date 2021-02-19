import unittest

from src.Runner import match

""" Test Class, feel free to add more tests or run using the CLI"""


class MatchSoftwareEngineerTest(unittest.TestCase):
    @staticmethod
    def test_automation_engineer():
        match(['-t', 'engineer', '-s', 'java', '-s', 'selenium'])

    @staticmethod
    def test_software_engineer():
        match(['-t', 'software'])

    @staticmethod
    def test_no_skills():
        match(['-t', 'engineer'])

    @staticmethod
    def test_automation_engineer_no_match():
        """ This test will not find a match since there is no Automation Engineer with Hadoop in it's skills"""
        match(['-t', 'engineer', '-s', 'java', '-s', 'selenium', '-s', 'hadoop'])


if __name__ == '__main__':
    unittest.main()
