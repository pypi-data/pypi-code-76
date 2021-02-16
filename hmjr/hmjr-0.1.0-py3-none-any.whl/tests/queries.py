import unittest
from hmjr import Entries

class TestEntries(unittest.TestCase):

    def testQueryEntriesByDate(self):
        data = Entries().withDate({
            "day": 5,
            "month": 5,
            "year": 44
        }).results
        self.assertIsNotNone(data)

    def testQueryEntriesByKeyword(self):
        data = Entries().withKeyword("camp").results
        self.assertIsNotNone(data)

    def testQueryEntriesByBook(self):
        data = Entries().withBook("001").results
        self.assertIsNotNone(data)

    def testQueryEntriesAll(self):
        data = Entries().all().results
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
