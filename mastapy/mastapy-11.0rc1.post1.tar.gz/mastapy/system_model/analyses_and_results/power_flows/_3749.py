'''_3749.py

FEPartPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2126
from mastapy.system_model.analyses_and_results.static_loads import _6517
from mastapy.system_model.analyses_and_results.power_flows import _3693
from mastapy._internal.python_net import python_net_import

_FE_PART_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FEPartPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartPowerFlow',)


class FEPartPowerFlow(_3693.AbstractShaftOrHousingPowerFlow):
    '''FEPartPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FE_PART_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def speed(self) -> 'float':
        '''float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Speed

    @property
    def fe_parts_are_not_used_in_power_flow_select_component_replaced_by_this_fe(self) -> 'str':
        '''str: 'FEPartsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEPartsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE

    @property
    def fe_parts_are_not_used_in_power_flow(self) -> 'str':
        '''str: 'FEPartsAreNotUsedInPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEPartsAreNotUsedInPowerFlow

    @property
    def component_design(self) -> '_2126.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6517.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6517.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
