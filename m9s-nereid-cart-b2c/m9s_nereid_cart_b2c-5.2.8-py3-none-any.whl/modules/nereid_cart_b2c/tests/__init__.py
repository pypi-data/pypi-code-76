# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.nereid_cart_b2c.tests.test_nereid_cart_b2c import (
        suite, create_website, create_countries, create_pricelists,
        create_product_template)
except ImportError:
    from .test_nereid_cart_b2c import (
        suite, create_website, create_countries, create_pricelists,
        create_product_template)

__all__ = ['suite', 'create_website', 'create_countries',
    'create_pricelists', 'create_product_template']
