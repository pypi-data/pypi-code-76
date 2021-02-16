import unittest
from hmjr import Entries
from hmjr import By

class TestEntries(unittest.TestCase):

    def testSortEntriesByHeader(self):
        data = Entries().withBook("708").sorted(By.header)
        self.assertIsNotNone(data)

    def testSortEntriesByDate(self):
        data = Entries().withBook("708").sorted(By.date)
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
