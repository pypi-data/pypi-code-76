# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import ModelView, fields


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    payment_profiles = fields.One2Many(
        'party.payment_profile', 'party', 'Payment Profiles'
    )
    default_payment_profile = fields.Function(
        fields.Many2One('party.payment_profile', 'Default Payment Profile'),
        'get_default_payment_profile'
    )

    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()
        cls._buttons.update({
            'add_payment_profile': {}
        })

    @classmethod
    @ModelView.button_action('payment_gateway.wizard_add_payment_profile')
    def add_payment_profile(cls, parties):
        pass

    def get_default_payment_profile(self, name):
        """
        Gets the payment profile with the lowest sequence,
        as in 1 is the highest priority and sets it
        """
        return self.payment_profiles and self.payment_profiles[0].id or None


class PartyErase(metaclass=PoolMeta):
    __name__ = 'party.erase'

    def to_erase(self, party_id):
        pool = Pool()
        PaymentProfile = pool.get('party.payment_profile')

        to_erase = super(PartyErase, self).to_erase(party_id)
        to_erase += [
            (PaymentProfile, [('party', '=', party_id)], True,
                ['name', 'provider_reference', 'last_4_digits', 'expiry_month',
                    'expiry_year'],
                [None, '****' , '****', '01', '2000']),
            ]
        return to_erase
