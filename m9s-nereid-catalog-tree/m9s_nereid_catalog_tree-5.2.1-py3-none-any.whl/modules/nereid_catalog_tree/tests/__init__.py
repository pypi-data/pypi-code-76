# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.nereid_catalog_tree.tests.test_nereid_catalog_tree import suite
except ImportError:
    from .test_nereid_catalog_tree import suite

__all__ = ['suite']
