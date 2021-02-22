# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.modules.company.model import CompanyValueMixin


default_customer_tax_rule = fields.Many2One(
    'account.tax.rule', 'Default Customer Tax Rule',
    domain=[
        ('kind', '=', 'sale'),
        ('company', '=', Eval('context', {}).get('company', -1)),
        ])

default_supplier_tax_rule = fields.Many2One(
    'account.tax.rule', 'Default Supplier Tax Rule',
    domain=[
        ('kind', '=', 'purchase'),
        ('company', '=', Eval('context', {}).get('company', -1)),
        ])


class Configuration(metaclass=PoolMeta):
    __name__ = 'account.configuration'

    default_customer_tax_rule = fields.MultiValue(
        default_customer_tax_rule)
    default_supplier_tax_rule = fields.MultiValue(
        default_supplier_tax_rule)

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'default_customer_tax_rule', 'default_supplier_tax_rule'}:
            return pool.get('account.configuration.default_tax_rule')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationDefaultTaxRule(ModelSQL, CompanyValueMixin):
    'Account Configuration Default Tax Rule'
    __name__ = 'account.configuration.default_tax_rule'

    default_customer_tax_rule = default_customer_tax_rule
    default_supplier_tax_rule = default_supplier_tax_rule
