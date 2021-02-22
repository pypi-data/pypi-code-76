'''_6273.py

RootAssemblyCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model import _2147
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _2296, _6184
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'RootAssemblyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCriticalSpeedAnalysis',)


class RootAssemblyCriticalSpeedAnalysis(_6184.AssemblyCriticalSpeedAnalysis):
    '''RootAssemblyCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2147.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2147.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def critical_speed_analysis_inputs(self) -> '_2296.CriticalSpeedAnalysis':
        '''CriticalSpeedAnalysis: 'CriticalSpeedAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2296.CriticalSpeedAnalysis)(self.wrapped.CriticalSpeedAnalysisInputs) if self.wrapped.CriticalSpeedAnalysisInputs else None
