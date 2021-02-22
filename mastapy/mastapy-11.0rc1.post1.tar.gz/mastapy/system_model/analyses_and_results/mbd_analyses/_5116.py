'''_5116.py

MeasurementComponentMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2136
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6551
from mastapy.system_model.analyses_and_results.mbd_analyses import _5167
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MeasurementComponentMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentMultibodyDynamicsAnalysis',)


class MeasurementComponentMultibodyDynamicsAnalysis(_5167.VirtualComponentMultibodyDynamicsAnalysis):
    '''MeasurementComponentMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2136.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6551.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6551.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
