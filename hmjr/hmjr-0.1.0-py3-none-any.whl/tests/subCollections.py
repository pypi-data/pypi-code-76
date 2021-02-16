
import unittest
from hmjr import Entries

class TestSubCollections(unittest.TestCase):

    def testSubCollectionDates(self):
        data = Entries().withBook("708", max=5).dates()
        self.assertIsNotNone(data)

    def testSubCollectionIndexes(self):
        data = Entries().withBook("708", max=5).indexes()
        self.assertIsNotNone(data)

    def testSubCollectionHeaders(self):
        data = Entries().withBook("708", max=5).headers()
        self.assertIsNotNone(data)

    def testSubCollectionContent(self):
        data = Entries().withBook("708", max=5).content()
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
