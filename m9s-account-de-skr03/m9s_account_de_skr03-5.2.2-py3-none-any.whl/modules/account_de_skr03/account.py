# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from sql import Table

from trytond.model import fields
from trytond.pyson import If, Eval, Bool
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    @classmethod
    def __register__(cls, module_name):
        cursor = Transaction().connection.cursor()
        model_data = Table('ir_model_data')

        # Migration from 5.6: Rename main tax ids
        if module_name == 'account_de_skr03':
            for old_id, new_id in (
                    ('tax_ust_19', 'tax_ust_standard_rate'),
                    ('tax_ust_7', 'tax_ust_reduced_rate'),
                    ('tax_vst_19', 'tax_vst_standard_rate'),
                    ('tax_vst_7', 'tax_vst_reduced_rate'),
                    ('tax_eu_19_purchase', 'tax_purchase_eu_standard_rate'),
                    ('tax_eu_7_purchase', 'tax_purchase_eu_reduced_rate'),
                    ('tax_import_19', 'tax_import_standard_rate'),
                    ('tax_import_7', 'tax_import_reduced_rate'),
                    ):
                cursor.execute(*model_data.select(model_data.id,
                        where=(model_data.fs_id == new_id)
                        & (model_data.module == module_name)))
                if cursor.fetchone():
                    continue
                cursor.execute(*model_data.update(
                        columns=[model_data.fs_id],
                        values=[new_id],
                        where=(model_data.fs_id == old_id)
                        & (model_data.module == module_name)))

        super().__register__(module_name)


def AccountTypeMixin(template=False):

    class Mixin:
        other = fields.Boolean(
            "Other",
            domain=[
                If(~Eval('statement').in_(['off-balance', 'balance']),
                    ('other', '=', False), ()),
                ],
            states={
                'invisible': ~Eval('statement').in_(
                    ['off-balance', 'balance']),
                },
            depends=['statement'])
    if not template:
        for fname in dir(Mixin):
            field = getattr(Mixin, fname)
            if not isinstance(field, fields.Field):
                continue
            field.states['readonly'] = (
                Bool(Eval('template', -1)) & ~Eval('template_override', False))
    return Mixin


class AccountTypeTemplate(AccountTypeMixin(template=True), metaclass=PoolMeta):
    __name__ = 'account.account.type.template'

    def _get_type_value(self, type=None):
        values = super()._get_type_value(type=type)
        if not type or type.other != self.other:
            values['other'] = self.other
        return values


class AccountType(AccountTypeMixin(), metaclass=PoolMeta):
    __name__ = 'account.account.type'
