# Originally auto-generated on 2021-02-15-12:09:58 -0500 EST
# By '--verbose --verbose x7.lib.patch'

from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib import patch


@tests(patch)
class TestModPatch(TestCase):
    """Tests for stand-alone functions in x7.lib.patch module"""

    @tests(patch.patch_base_class)
    def test_patch_base_class(self):
        # patch_base_class(name, bases, namespace)
        class Base:
            # noinspection PyMethodMayBeStatic
            def some_method(self):
                return 'original'

        b = Base()
        self.assertEqual('original', b.some_method())

        class Derived(Base, metaclass=patch.patch_base_class):
            def some_method(self):
                return 'patched'

        self.assertEqual('patched', b.some_method())
        with self.assertRaises(TypeError):
            Derived()
