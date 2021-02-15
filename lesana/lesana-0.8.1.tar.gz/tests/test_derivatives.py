import shutil
import tempfile
import unittest

import lesana
from lesana import types
from . import utils


class DerivedType(types.LesanaString):
    """
    A custom type
    """
    name = 'derived'


class Derivative(lesana.Collection):
    """
    A class serived from lesana.Collection
    """


class testDerivatives(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        utils.copytree(
            'tests/data/derivative',
            self.tmpdir,
            dirs_exist_ok=True
        )
        self.collection = Derivative(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_load_subclasses(self):
        self.assertIsInstance(self.collection.fields['unknown'], DerivedType)


if __name__ == '__main__':
    unittest.main()
