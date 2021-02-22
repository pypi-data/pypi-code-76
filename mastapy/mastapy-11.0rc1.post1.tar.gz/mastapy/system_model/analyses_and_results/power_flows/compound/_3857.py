'''_3857.py

ConicalGearCompoundPowerFlow
'''


from mastapy.gears.rating.conical import _485
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows.compound import _3883
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConicalGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundPowerFlow',)


class ConicalGearCompoundPowerFlow(_3883.GearCompoundPowerFlow):
    '''ConicalGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_485.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_485.ConicalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def conical_gear_duty_cycle_rating(self) -> '_485.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'ConicalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_485.ConicalGearDutyCycleRating)(self.wrapped.ConicalGearDutyCycleRating) if self.wrapped.ConicalGearDutyCycleRating else None
