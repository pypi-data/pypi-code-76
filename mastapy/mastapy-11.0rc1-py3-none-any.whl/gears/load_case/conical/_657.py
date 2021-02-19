'''_657.py

ConicalGearSetLoadCase
'''


from mastapy.gears.load_case import _645
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Conical', 'ConicalGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetLoadCase',)


class ConicalGearSetLoadCase(_645.GearSetLoadCaseBase):
    '''ConicalGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
