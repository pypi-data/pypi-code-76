'''_4349.py

TorqueConverterModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2278
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6605
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4269
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'TorqueConverterModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterModalAnalysisAtAStiffness',)


class TorqueConverterModalAnalysisAtAStiffness(_4269.CouplingModalAnalysisAtAStiffness):
    '''TorqueConverterModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2278.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6605.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6605.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
