'''_3700.py

BearingPowerFlow
'''


from mastapy.system_model.part_model import _2114
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6451
from mastapy.bearings.bearing_results.rolling import _1764
from mastapy.system_model.analyses_and_results.power_flows import _3728
from mastapy._internal.python_net import python_net_import

_BEARING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BearingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingPowerFlow',)


class BearingPowerFlow(_3728.ConnectorPowerFlow):
    '''BearingPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEARING_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6451.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6451.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def rolling_bearing_speed_results(self) -> '_1764.RollingBearingSpeedResults':
        '''RollingBearingSpeedResults: 'RollingBearingSpeedResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1764.RollingBearingSpeedResults)(self.wrapped.RollingBearingSpeedResults) if self.wrapped.RollingBearingSpeedResults else None
