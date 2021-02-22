'''_3816.py

TorqueConverterTurbinePowerFlow
'''


from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6607
from mastapy.system_model.analyses_and_results.power_flows import _3730
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'TorqueConverterTurbinePowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbinePowerFlow',)


class TorqueConverterTurbinePowerFlow(_3730.CouplingHalfPowerFlow):
    '''TorqueConverterTurbinePowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbinePowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2281.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6607.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6607.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
