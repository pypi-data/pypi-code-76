'''_6628.py

BoltedJointAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model import _2092
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6429
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6707
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'BoltedJointAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointAdvancedTimeSteppingAnalysisForModulation',)


class BoltedJointAdvancedTimeSteppingAnalysisForModulation(_6707.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation):
    '''BoltedJointAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2092.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6429.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6429.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
