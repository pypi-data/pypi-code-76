'''_3517.py

RollingRingAssemblyStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2268
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6574
from mastapy.system_model.analyses_and_results.stability_analyses import _3524
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RollingRingAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyStabilityAnalysis',)


class RollingRingAssemblyStabilityAnalysis(_3524.SpecialisedAssemblyStabilityAnalysis):
    '''RollingRingAssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2268.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2268.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6574.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
