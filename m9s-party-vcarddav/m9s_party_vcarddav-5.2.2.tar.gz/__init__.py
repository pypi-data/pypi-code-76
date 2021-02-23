# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
# from . import carddav
from . import webdav
from . import party

__all__ = ['register']


def register():
    Pool.register(
        webdav.Collection,
        party.Party,
        party.Address,
        party.ActionReport,
        module='party_vcarddav', type_='model')
    Pool.register(
        party.VCard,
        module='party_vcarddav', type_='report')
