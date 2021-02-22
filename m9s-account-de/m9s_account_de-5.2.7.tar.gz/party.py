# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    @classmethod
    def default_customer_tax_rule(cls, **pattern):
        pool = Pool()
        Configuration = pool.get('account.configuration')
        config = Configuration(1)
        rule = config.get_multivalue(
            'default_customer_tax_rule', **pattern)
        return rule and rule.id

    @classmethod
    def default_supplier_tax_rule(cls, **pattern):
        pool = Pool()
        Configuration = pool.get('account.configuration')
        config = Configuration(1)
        rule = config.get_multivalue(
            'default_supplier_tax_rule', **pattern)
        return rule and rule.id
