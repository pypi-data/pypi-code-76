# Originally auto-generated on 2020-02-09-22:46:15 -0500 EST
# By '--verbose --verbose gg.animate.edit.bidict'

from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib.bidict import BidirectionalUniqueDictionary


@tests(BidirectionalUniqueDictionary)
class TestBidirectionalUniqueDictionary(TestCase):
    @tests(BidirectionalUniqueDictionary.__init__)
    @tests(BidirectionalUniqueDictionary.__delitem__)
    @tests(BidirectionalUniqueDictionary.__setitem__)
    def test_basic(self):
        """Test that things work"""
        a = BidirectionalUniqueDictionary()
        a[3] = 4
        self.assertEqual(4, a[3])
        self.assertEqual(3, a.inverse[4])
        a[2] = 5
        self.assertEqual(4, a[3])
        self.assertEqual(3, a.inverse[4])
        self.assertEqual(5, a[2])
        self.assertEqual(2, a.inverse[5])

        self.assertEqual({3: 4, 2: 5}, a)
        self.assertEqual({4: 3, 5: 2}, a.inverse)
        a[3.0] = 4.0
        self.assertEqual({3: 4, 2: 5}, a)
        self.assertEqual({4: 3, 5: 2}, a.inverse)
        # self.assertEqual({3.0: 4.0, 2: 5}, a)
        # self.assertEqual({4.0: 3.0, 5: 2}, a.inverse)

        self.assertIn(3, a)
        del a[3]
        self.assertEqual({2: 5}, a)
        self.assertEqual({5: 2}, a.inverse)

    def test_errors(self):
        """Things that shouldn't work"""
        with self.assertRaises(ValueError):
            BidirectionalUniqueDictionary(a=3, b=3)

        a = BidirectionalUniqueDictionary()
        a[3] = 4
        with self.assertRaises(ValueError):
            a[2] = 4
        self.assertEqual({3: 4}, a)
        a[4] = 5
        with self.assertRaises(ValueError):
            a[3] = 5
