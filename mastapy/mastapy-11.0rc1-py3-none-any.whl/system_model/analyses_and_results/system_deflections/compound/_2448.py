'''_2448.py

ConicalGearCompoundSystemDeflection
'''


from typing import List

from mastapy.gears.rating.conical import _321
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2470
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConicalGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundSystemDeflection',)


class ConicalGearCompoundSystemDeflection(_2470.GearCompoundSystemDeflection):
    '''ConicalGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self) -> '_321.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_321.ConicalGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def conical_duty_cycle_rating(self) -> '_321.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'ConicalDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_321.ConicalGearDutyCycleRating)(self.wrapped.ConicalDutyCycleRating) if self.wrapped.ConicalDutyCycleRating else None

    @property
    def planetaries(self) -> 'List[ConicalGearCompoundSystemDeflection]':
        '''List[ConicalGearCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearCompoundSystemDeflection))
        return value
