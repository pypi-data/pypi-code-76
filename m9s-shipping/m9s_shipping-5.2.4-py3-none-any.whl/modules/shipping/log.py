# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields


class CarrierLog(ModelSQL, ModelView):
    "Carrier Log"
    __name__ = 'carrier.log'

    sale = fields.Many2One('sale.sale', 'Sale', readonly=True)
    shipment_out = fields.Many2One(
        'stock.shipment.out', 'Shipment Out', readonly=True
    )
    carrier = fields.Many2One(
        'carrier', 'Carrier', required=True, readonly=True
    )
    log = fields.Text('Log', required=True, readonly=True)
