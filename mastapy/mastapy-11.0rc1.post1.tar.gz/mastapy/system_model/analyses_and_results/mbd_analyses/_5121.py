'''_5121.py

PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2260
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.mbd_analyses import _5070
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PartToPartShearCouplingHalfMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfMultibodyDynamicsAnalysis',)


class PartToPartShearCouplingHalfMultibodyDynamicsAnalysis(_5070.CouplingHalfMultibodyDynamicsAnalysis):
    '''PartToPartShearCouplingHalfMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2260.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2260.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6559.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
