'''_3707.py

BevelDifferentialSunGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2189
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3704
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BevelDifferentialSunGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearPowerFlow',)


class BevelDifferentialSunGearPowerFlow(_3704.BevelDifferentialGearPowerFlow):
    '''BevelDifferentialSunGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2189.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
