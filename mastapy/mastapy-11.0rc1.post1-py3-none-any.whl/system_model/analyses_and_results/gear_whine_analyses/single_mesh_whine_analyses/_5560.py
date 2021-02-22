'''_5560.py

PowerLoadSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2072
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6236
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5594
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PowerLoadSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadSingleMeshWhineAnalysis',)


class PowerLoadSingleMeshWhineAnalysis(_5594.VirtualComponentSingleMeshWhineAnalysis):
    '''PowerLoadSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2072.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2072.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6236.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6236.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
