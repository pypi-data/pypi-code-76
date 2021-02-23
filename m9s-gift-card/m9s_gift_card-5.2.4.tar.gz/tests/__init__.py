# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.gift_card.tests.test_gift_card import suite
except ImportError:
    from .test_gift_card import suite

__all__ = ['suite']
