# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import currency
from . import party
from . import tax

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        configuration.ConfigurationDefaultTaxRule,
        party.Party,
        tax.AdvanceTurnoverTaxReturnContext,
        tax.TaxCode,
        currency.Currency,
        module='account_de', type_='model')
    Pool.register(
        tax.AdvanceTurnoverTaxReturnReport,
        module='account_de', type_='report')
