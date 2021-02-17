# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import copy
from decimal import Decimal
from trytond.model import ModelView, fields
from trytond.pyson import Eval
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta


class TaxCode(metaclass=PoolMeta):
    __name__ = 'account.tax.code'

    @classmethod
    def get_sum(cls, codes, name):
        period_ids = cls.get_period_ids()
        with Transaction().set_context(periods=period_ids):
            return super(TaxCode, cls).get_sum(codes, name)

    @classmethod
    def get_period_ids(cls):
        pool = Pool()
        Period = pool.get('account.period')
        context = Transaction().context

        start_period = end_period = None
        if context.get('start_period'):
            start_period = Period(context['start_period'])
        if context.get('end_period'):
            end_period = Period(context['end_period'])

        period_ids = []
        if start_period or end_period:
            search_clause = [
                ('fiscalyear', '=', context.get('fiscalyear')),
                ]
            if start_period:
                search_clause.append(
                    ('start_date', '>=', start_period.start_date))
            if end_period:
                search_clause.append(
                    ('end_date', '<=', end_period.end_date))

            periods = Period.search(search_clause)
            if periods:
                period_ids = [p.id for p in periods]
        return period_ids


class AdvanceTurnoverTaxReturnContext(ModelView):
    'Advance Turnover Tax Return Context'
    __name__ = 'tax.advance_turnover_tax_return.context'
    fiscalyear = fields.Many2One('account.fiscalyear', 'Fiscal Year',
        required=True)
    start_period = fields.Many2One('account.period', 'Start Period',
        domain=[
            ('fiscalyear', '=', Eval('fiscalyear')),
            ('start_date', '<=', (Eval('end_period'), 'start_date'))
            ],
        depends=['end_period', 'fiscalyear'])
    end_period = fields.Many2One('account.period', 'End Period',
        domain=[
            ('fiscalyear', '=', Eval('fiscalyear')),
            ('start_date', '>=', (Eval('start_period'), 'start_date')),
            ],
        depends=['start_period', 'fiscalyear'])
    company = fields.Many2One('company.company', 'Company', required=True)
    show_empty_lines = fields.Boolean('Show empty lines',
        help='Show/print also lines with zero amount.')

    @staticmethod
    def default_fiscalyear():
        FiscalYear = Pool().get('account.fiscalyear')
        return FiscalYear.find(
            Transaction().context.get('company'), exception=False)

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_show_empty_lines():
        return False

    @fields.depends('fiscalyear')
    def on_change_fiscalyear(self):
        self.start_period = None
        self.end_period = None


class AdvanceTurnoverTaxReturnReport(Report):
    __name__ = 'tax.advance_turnover_tax_return'

    @classmethod
    def get_context(cls, records, data):
        pool = Pool()
        Company = pool.get('company.company')
        Fiscalyear = pool.get('account.fiscalyear')
        Period = pool.get('account.period')
        context = Transaction().context

        report_context = super(
            AdvanceTurnoverTaxReturnReport, cls).get_context(records, data)

        report_context['company'] = Company(context['company'])
        report_context['fiscalyear'] = Fiscalyear(context['fiscalyear'])

        for period in ['start_period', 'end_period']:
            if context.get(period):
                report_context[period] = Period(context[period])
            else:
                report_context[period] = None

        def get_prefix(record, prefix=''):
            new_prefix = prefix
            if record.parent:
                if record.childs and not new_prefix:
                    new_prefix += str('⤵', 'utf-8')
                else:
                    new_prefix = str('͏⟝', 'utf-8') + new_prefix
                new_prefix = get_prefix(record.parent, new_prefix)
            return new_prefix

        accounts = []
        for record in records:
            if not context['show_empty_lines']:
                if record.sum == Decimal('0.0'):
                    continue
            new_record = copy.deepcopy(record)
            new_record.name = get_prefix(record) + ' ' + record.name
            accounts.append(new_record)

        report_context['accounts'] = accounts
        return report_context
