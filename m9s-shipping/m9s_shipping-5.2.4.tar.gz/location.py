# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval


class Location(metaclass=PoolMeta):
    __name__ = "stock.location"

    return_address = fields.Many2One(
        "party.address", "Return Address", states={
            'invisible': Eval('type') != 'warehouse',
            'readonly': ~Eval('active'),
        }, depends=['type', 'active'],
        help="Return undelivered shipments to this address"
    )
