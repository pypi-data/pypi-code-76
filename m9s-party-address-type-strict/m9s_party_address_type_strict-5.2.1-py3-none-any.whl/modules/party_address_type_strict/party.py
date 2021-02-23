# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def create(cls, vlist):
        vlist = [v.copy() for v in vlist]
        for values in vlist:
            for addr_type in ['invoice', 'delivery']:
                if values.get(addr_type) is True:
                    addr2update = cls.search([
                            ('party', '=', values['party']),
                            (addr_type, '=', True),
                            ])
                    if addr2update:
                        cls.write(addr2update, {
                                addr_type: False,
                                })
        return super(Address, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for addresses, values in zip(actions, actions):
            for addr_type in ['invoice', 'delivery']:
                if values.get(addr_type) is True:
                    address = addresses[0]
                    addr2update = cls.search([
                            ('party', '=', address.party),
                            (addr_type, '=', True),
                            ('id', '!=', address.id),
                            ])
                    if addr2update:
                        cls.write(addr2update, {
                                addr_type: False,
                                })
            args.extend((addresses, values))
        super(Address, cls).write(*args)
