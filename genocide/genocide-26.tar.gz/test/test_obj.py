# This file is placed in the Public Domain.

import types, unittest

from op.dbs import last
from op.obj  import O, Object, load, save

class Obj(O):
    def test(self):
        return True

class Test_Object(unittest.TestCase):

    def test_clean(self):
        o = Obj()
        self.assertTrue("test" not in o.__dict__)

    def test_notclean(self):
        class Obj(O):
            def test(self):
                return True
        o = Obj()
        self.assertTrue("test" in dir(o))

    def test_attr(self):
        o = Obj()
        o.test = "bla"
        self.assertTrue(type(o.test) != types.MethodType)        
                
    def test_O(self):
        o = O()
        self.assertEqual(type(o), O)

    def test_Object(self):
        o = Object()
        self.assertTrue(isinstance(o, Object))

    def test_intern1(self):
        o = Object()
        self.assertTrue(o.__type__)

    def test_intern2(self):
        o = Object()
        self.assertFalse(o)

    def test_intern3(self):
        o = Object()
        self.assertTrue("<op.obj.Object object at" in repr(o))

    def test_intern4(self):
        o = Object()
        self.assertTrue(o.__type__ in str(type(o)))

    def test_intern5(self):
        o = Object()
        self.assertTrue(o.__id__)

    def test_empty(self):
        o = Object()
        self.assertTrue(not o)

    def test_final(self):
        o = Object()
        o.last = "bla"
        last(o)
        self.assertEqual(o.last, "bla")

    def test_stamp(self):
        o = Object()
        save(o)
        self.assertTrue(o.__type__)

    def test_attribute(self):
        o = Object()
        o.bla = "test"
        p = save(o)
        oo = Object()
        load(oo, p)
        self.assertEqual(oo.bla, "test")

    def test_changeattr(self):
        o = Object()
        o.bla = "test"
        p = save(o)
        oo = Object()
        load(oo, p)
        oo.bla = "mekker"
        pp = save(oo)
        ooo = Object()
        load(ooo, pp)
        self.assertEqual(ooo.bla, "mekker")

    def test_last(self):
        o = Object()
        o.bla = "test"
        save(o)
        oo = Object()
        last(oo)
        self.assertEqual(oo.bla, "test")

    def test_lastest(self):
        o = Object()
        o.bla = "test"
        save(o)
        oo = Object()
        last(oo)
        oo.bla = "mekker"
        save(oo)
        ooo = Object()
        last(ooo)
        self.assertEqual(ooo.bla, "mekker")
