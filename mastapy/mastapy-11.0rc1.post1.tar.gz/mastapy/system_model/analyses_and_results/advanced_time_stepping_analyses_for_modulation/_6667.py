'''_6667.py

ConceptCouplingAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.couplings import _2252
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6471
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6678
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'ConceptCouplingAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingAdvancedTimeSteppingAnalysisForModulation',)


class ConceptCouplingAdvancedTimeSteppingAnalysisForModulation(_6678.CouplingAdvancedTimeSteppingAnalysisForModulation):
    '''ConceptCouplingAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2252.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6471.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6471.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
