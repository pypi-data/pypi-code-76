import sys
from io import StringIO
from unittest import TestCase
from x7.lib.annotations import tests
from x7.testing.support import Capture, Argv, Pickler, PicklerExtensionImage, PicklerExtension
from x7.testing import support
# noinspection PyPackageRequirements
from PIL import Image


@tests(Capture)
class TestCapture(TestCase):
    @tests(Capture.__enter__)
    @tests(Capture.__exit__)
    @tests(Capture.__init__)
    @tests(Capture.stderr)
    @tests(Capture.stdout)
    def test_capture(self):
        with Capture() as cm:
            print('StdOut', file=sys.stdout)
            print('StdErr', file=sys.stderr)
        self.assertIn('StdOut', cm.stdout())
        self.assertIn('StdErr', cm.stderr())


@tests(Argv)
class TestArgv(TestCase):
    @tests(Argv.__enter__)
    @tests(Argv.__exit__)
    @tests(Argv.__init__)
    def test_argv(self):
        old = sys.argv
        with Argv(['something', 'else']):
            self.assertEqual(['something', 'else'], sys.argv)
        self.assertEqual(old, sys.argv)


class SimpleObject:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x


class PrimitivePoint:
    """Test class for adding additional primitive"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __repr__(self):
        return 'PrimitivePoint(%r, %r)' % (self.x, self.y)


class PicklerExtensionPP(PicklerExtension):
    """
        Helper object to add PIL.Image type to Pickler
    """

    def __init__(self, pickler: 'Pickler'):
        super().__init__(pickler)
        self.primitives = (PrimitivePoint, )
        # self.types = (Image.Image, )

    def methods(self):
        return dict(PrimitivePoint=PrimitivePoint)


@tests(support.Pickler)
class TestPickler(TestCase):
    @tests(support.Pickler.__init__)
    @tests(support.Pickler.vars_for_load)
    def test___init__(self):
        self.assertIsNotNone(Pickler())
        self.assertIsNotNone(Pickler(PicklerExtensionImage))
        self.assertIsNotNone(Pickler(PicklerExtensionPP))
        self.assertIsNotNone(Pickler((PicklerExtensionImage, PicklerExtensionPP)))
        with self.assertRaisesRegex(ValueError, 'duplicate function names: image'):
            Pickler((PicklerExtensionImage, PicklerExtensionImage))
        with self.assertRaisesRegex(ValueError, 'duplicate function names: image, image'):
            Pickler((PicklerExtensionImage, PicklerExtensionImage, PicklerExtensionImage))

    @tests(support.Pickler.bytes_in)
    @tests(support.Pickler.bytes_out)
    def test_bytes_in_out(self):
        pickler = Pickler()
        a = b'\xF0foobar\xFF\x00spam'
        b = pickler.bytes_out(a)
        c = pickler.bytes_in(eval(b, {}))
        self.assertEqual(a, c)

    @tests(support.Pickler.obj_in)
    @tests(support.Pickler.obj_out)
    def test_bytes_in_out(self):
        pickler = Pickler()
        a = dict(a=3, b='foobar', c=[3, 4])
        b = pickler.obj_out(a)
        c = pickler.obj_in(eval(b, {}))
        self.assertEqual(a, c)

    @tests(support.Pickler.do_pickle)
    @tests(support.Pickler.do_pickle_dict)
    @tests(support.Pickler.dump_dict)
    @tests(support.Pickler.do_pickle_extensions)
    @tests(support.Pickler.is_simple)
    @tests(support.Pickler.pickled)
    def test_do_pickle(self):
        def pu(data, expected=None, extensions=(), startswith=None):
            pickler = Pickler(extensions)
            pickled = pickler.do_pickle(data, '  ')
            # print(pickled)
            if expected:
                self.assertEqual(pickled, expected)
            if startswith:
                self.assertTrue(pickled.startswith(startswith), 'Expected %r to start with %r' % (pickled, startswith))
            sio = StringIO(pickled)
            self.assertEqual(data, pickler.load(sio))
            return pickled
        pu(1, '1')
        pu('foo', "'foo'")
        pu([1, 'foo'], "[1, 'foo']")
        pu(dict(a='bar', c=3, d=[1, 7]), "{'a': 'bar', 'c': 3, 'd': [1, 7]}")
        pu(SimpleObject(17))
        # noinspection SpellCheckingInspection
        pu(dict(a=SimpleObject(21), c=3, d=[1, 7]), """{
      'a': pickled('SimpleObject', 'c${lsnQG4f0X?!Msl_G5dKKn+AVy|hI+%_xE-fg?FDjYR!xNmDTac6LpOlrFTry?y6wSsdwNrW+E2emh7ANTe0EE~Yn*'),
      'c': 3,
      'd': [1, 7],
}""")

        # With no extension, just outputs a pickled object
        pu(Image.new('1', (1, 1), 'black'), startswith="pickled('Image',")
        pu(Image.new('RGBA', (2, 2), 'yellow'), startswith="pickled('Image',")

        # With extension, outputs a call to image
        pu(Image.new('1', (1, 1), 'black'), extensions=PicklerExtensionImage, startswith="image('1', (1, 1),")
        pu(Image.new('RGBA', (2, 2), 'yellow'), extensions=PicklerExtensionImage, startswith="image('RGBA', (2, 2), ")

        # With extension, outputs a call to PrimitivePoint
        pu(PrimitivePoint(1, 2), startswith="pickled('PrimitivePoint',")
        pu(PrimitivePoint(1, 2), 'PrimitivePoint(1, 2)', extensions=PicklerExtensionPP)

    @tests(support.Pickler.load)
    def test_load(self):
        # load(self, in_file)
        pass  # TODO-impl x7.testing.support.Pickler.load test


@tests(support.RecordedData)
class TestRecordedData(TestCase):
    pass


@tests(support.RecordedDataModule)
class TestRecordedDataModule(TestCase):
    @tests(support.RecordedDataModule.__init__)
    def test___init__(self):
        # __init__(self, mod: str)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.__init__ test

    @tests(support.RecordedDataModule._key)
    def test__key(self):
        # _key(cls, func, case)
        pass  # TODO-impl x7.testing.support.RecordedDataModule._key test

    @tests(support.RecordedDataModule.file_name)
    def test_file_name(self):
        # file_name(self)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.file_name test

    @tests(support.RecordedDataModule.get)
    def test_get(self):
        # get(self, cls, func: str, case: str)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.get test

    @tests(support.RecordedDataModule.load)
    def test_load(self):
        # load(self)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.load test

    @tests(support.RecordedDataModule.put)
    def test_put(self):
        # put(self, cls, func: str, case: str, new_data)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.put test

    @tests(support.RecordedDataModule.save)
    def test_save(self):
        # save(self)
        pass  # TODO-impl x7.testing.support.RecordedDataModule.save test


@tests(support.RecorderError)
class TestRecorderError(TestCase):
    pass


@tests(support)
class Test0support(TestCase):
    """Tests for stand-alone functions in x7.testing.support module"""

    @tests(support.unused)
    def test_unused(self):
        # As this function is meant to bury unused variable lint warnings,
        # not much to test here, just call it with one or two vars
        support.unused(support)
        support.unused(self, support)

    @tests(support.warn_class)
    def test_warn_class(self):
        # warn_class(klass: type, message)
        pass  # TODO-impl x7.testing.support.warn_class test
