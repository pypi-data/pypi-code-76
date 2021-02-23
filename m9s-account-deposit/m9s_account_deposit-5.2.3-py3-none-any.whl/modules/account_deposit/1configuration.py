# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from sql import Null
from sql.conditionals import Case

from trytond.pool import PoolMeta
from trytond.model import ModelView, ModelSQL, MatchMixin, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval

deposit_settlement_methods = [
    ('strict', 'Strict (Require complete deposit per invoice)'),
    ('partial', 'Partial (Allow partial deposit per invoice)'),
    ]


class Configuration(metaclass=PoolMeta):
    __name__ = 'account.configuration'

    default_account_deposit = fields.Property(fields.Many2One(
            'account.account', 'Default Account Deposit',
            domain=[
                ('kind', '=', 'deposit'),
                ('company', '=', Eval('context', {}).get('company', -1)),
                ]))

    deposit_settlement_method = fields.Property(fields.Selection(
            'account.account', 'Deposit Settlement Method',
            domain=[
                ('kind', '=', 'deposit'),
                ('company', '=', Eval('context', {}).get('company', -1)),
                ]))
    deposit_settlement_method = fields.Function(fields.Selection(
            deposit_settlement_methods, 'Deposit Settlement Method'),
        'on_change_with_deposit_settlement_method')
    deposit_settlement_methods = fields.One2Many(
        'account.configuration.deposit_settlement_method',
        'configuration', 'Deposit Settlement Methods')

    @classmethod
    def default_deposit_settlement_method(cls):
        return 'partial'

    @fields.depends('deposit_settlement_methods')
    def on_change_with_deposit_settlement_method(self, name=None,
            pattern=None):
        context = Transaction().context
        if pattern is None:
            pattern = {}
        pattern = pattern.copy()
        pattern['company'] = context.get('company')

        for line in self.deposit_settlement_methods:
            if line.match(pattern):
                return line.method
        return self.default_deposit_settlement_method()


class ConfigurationDepositSettlementMethod(ModelSQL, ModelView, MatchMixin):
    'Account Configuration Deposit Settlement Method'
    __name__ = 'account.configuration.deposit_settlement_method'
    configuration = fields.Many2One('account.configuration', 'Configuration',
        required=True, ondelete='CASCADE')
    sequence = fields.Integer('Sequence')
    company = fields.Many2One('company.company', 'Company')
    method = fields.Selection(deposit_settlement_methods, 'Method',
        required=True)

    @classmethod
    def __setup__(cls):
        super(ConfigurationDepositSettlementMethod, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @classmethod
    def order_sequence(cls, tables):
        table, _ = tables[None]
        return [Case((table.sequence == Null, 0), else_=1), table.sequence]

    @classmethod
    def default_method(cls):
        return 'partial'
