# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import account
from . import configuration
from . import contract
from . import invoice
from . import party


def register():
    Pool.register(
        account.AccountTypeTemplate,
        account.AccountType,
        configuration.Configuration,
        configuration.ConfigurationDefaultAccount,
        configuration.ConfigurationDepositSettlementMethod,
        invoice.Invoice,
        invoice.InvoiceLine,
        invoice.DepositRecallStart,
        party.Party,
        module='account_deposit', type_='model')
    Pool.register(
        contract.ContractConsumption,
        module='account_deposit', type_='model', depends=['contract'])
    Pool.register(
        invoice.DepositRecall,
        party.PartyErase,
        module='account_deposit', type_='wizard')
