# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.carrier_weight_volume_combined.tests.test_carrier_weight_volume_combined import suite
except ImportError:
    from .test_carrier_weight_volume_combined import suite

__all__ = ['suite']
