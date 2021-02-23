# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from functools import partial
from itertools import groupby
from decimal import Decimal

from trytond.model import ModelView, Workflow
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.tools import sortable_values
from trytond.exceptions import UserWarning
from trytond.i18n import gettext

from ._parcel import parcel_weight, parcel_volume


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    # check_volume_weight must not be performed in quote for webshop channels
    # to not raise user warnings in the checkout process.
    # Nevertheless provide the information for webshop orders at least on
    # the processing of the order.
    @classmethod
    @ModelView.button
    @Workflow.transition('quotation')
    def quote(cls, sales):
        if not Transaction().context.get('skip_volume_weight_check'):
            for sale in [s for s in sales
                    if (s.carrier and
                        s.carrier.carrier_cost_method == 'weight_volume')
                    and not (getattr(cls, 'channel_type', None)
                        and s.channel_type == 'webshop')]:
                sale.check_volume_weight()
        super(Sale, cls).quote(sales)

    @classmethod
    def process(cls, sales):
        if not Transaction().context.get('skip_volume_weight_check'):
            for sale in [s for s in sales
                    if (s.carrier and
                        s.carrier.carrier_cost_method == 'weight_volume')
                    and (getattr(cls, 'channel_type', None)
                        and s.channel_type == 'webshop')]:
                sale.check_volume_weight()
        super(Sale, cls).process(sales)

    def check_volume_weight(self):
        '''
        Warn if there are missing data for the correct carrier calculation.
        '''
        products = [line.product for line in self.lines or []
            if getattr(line, 'product', None)
            and line.product.type in ('goods', 'assets')
            and not (getattr(line.product, 'is_gift_card', None) and
                line.product.is_gift_card)
            and (not line.product.volume or not line.product.weight)]
        if products:
            product_names = ''
            for product in products:
                product_names += '%s\n' % product.rec_name
            warning_name = 'missing_weight_volume_sale_%s' % self.id
            raise UserWarning(warning_name,
                gettext('missing_weight_volume',
                    product_names))

    def _group_parcel_key(self, lines, line):
        """
        The key to group lines by parcel
        """
        return ()

    @fields.depends('carrier', 'moves',
        methods=['_group_parcel_key'])
    def _get_carrier_context(self):
        context = super(Sale, self)._get_carrier_context()

        if self.carrier.carrier_cost_method != 'weight_volume':
            return context

        lines = [l for l in self.lines or [] if l.quantity and l.quantity > 0]
        keyfunc = partial(self._group_parcel_key, lines)
        lines = sorted(lines, key=sortable_values(keyfunc))

        weights = []
        volumes = []
        parcel_group = []
        context['weights'] = weights
        context['volumes'] = volumes
        for key, parcel in groupby(lines, key=keyfunc):
            # Store iterator as list for re-use
            parcel_group = list(parcel)
            weights.append(parcel_weight(
                    parcel_group, self.carrier.weight_uom, 'unit'))
            volumes.append(parcel_volume(
                    parcel_group, self.carrier.volume_uom, 'unit'))
        return context

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        '''
        shipping:

        Gives a list of rates from provided carrier and carrier service.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'carrier_service': carrier.service active record,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        '''
        pool = Pool()
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')

        if carrier.carrier_cost_method == 'weight_volume':
            currency = Company(Transaction().context['company']).currency
            weight = Uom.compute_qty(self.weight_uom, self.weight,
                carrier.weight_uom)
            volume = Uom.compute_qty(self.volume_uom, self.volume,
                carrier.volume_uom)
            weight_cost = carrier.compute_weight_price(weight)
            volume_cost = carrier.compute_volume_price(volume)
            if weight_cost > Decimal(0) and volume_cost > Decimal(0):
                cost = max(weight_cost, volume_cost)
            else:
                return []
            rate_dict = {
                'carrier_service': carrier_service,
                'cost': cost,
                'cost_currency': currency,
                'carrier': carrier,
                'display_name': carrier.rec_name,
            }
            return [rate_dict]

        return super(Sale, self).get_shipping_rate(carrier,
            carrier_service=carrier_service, silent=silent)
