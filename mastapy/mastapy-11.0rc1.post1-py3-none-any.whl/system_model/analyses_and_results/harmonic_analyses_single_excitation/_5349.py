'''_5349.py

BoltedJointHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import _2117
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6462
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5429
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'BoltedJointHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointHarmonicAnalysisOfSingleExcitation',)


class BoltedJointHarmonicAnalysisOfSingleExcitation(_5429.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation):
    '''BoltedJointHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2117.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6462.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6462.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
