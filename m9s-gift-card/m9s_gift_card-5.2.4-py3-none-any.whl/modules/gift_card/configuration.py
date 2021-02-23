# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond import backend
from trytond.model import (ModelView, ModelSQL, ModelSingleton, ValueMixin,
    fields)
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

liability_account = fields.Many2One('account.account', 'Liability Account',
    required=True)
number_sequence = fields.Many2One('ir.sequence', 'Number Sequence',
    required=True, domain=[('code', '=', 'gift_card.gift_card')])


class Configuration(
        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
    "Configuration"
    __name__ = 'gift_card.configuration'

    liability_account = fields.MultiValue(liability_account)
    number_sequence = fields.MultiValue(number_sequence)


class _ConfigurationValue(ModelSQL):

    _configuration_value_field = None

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(_ConfigurationValue, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append(cls._configuration_value_field)
        value_names.append(cls._configuration_value_field)
        migrate_property(
            'gift_card.configuration', field_names, cls, value_names,
            fields=fields)


class GiftCardConfigurationSequence(_ConfigurationValue, ModelSQL, ValueMixin):
    'Gift Card Configuration Sequence'
    __name__ = 'gift_card.configuration.number_sequence'
    number_sequence = number_sequence
    _configuration_value_field = 'number_sequence'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class GiftCardLiabilityAccount(_ConfigurationValue, ModelSQL, ValueMixin):
    'Gift Card Liability Account'
    __name__ = 'gift_card.configuration.liability_account'
    liability_account = liability_account
    _configuration_value_field = 'liability_account'
