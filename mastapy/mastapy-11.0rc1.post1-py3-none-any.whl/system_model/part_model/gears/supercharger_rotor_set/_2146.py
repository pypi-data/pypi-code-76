'''_2146.py

SuperchargerRotorSetDatabase
'''


from mastapy.utility.databases import _1359
from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2145
from mastapy._internal.python_net import python_net_import

_SUPERCHARGER_ROTOR_SET_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'SuperchargerRotorSetDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('SuperchargerRotorSetDatabase',)


class SuperchargerRotorSetDatabase(_1359.NamedDatabase['_2145.SuperchargerRotorSet']):
    '''SuperchargerRotorSetDatabase

    This is a mastapy class.
    '''

    TYPE = _SUPERCHARGER_ROTOR_SET_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SuperchargerRotorSetDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
