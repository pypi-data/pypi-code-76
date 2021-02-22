'''_5954.py

CVTPulleyDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2258
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6001
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CVTPulleyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyDynamicAnalysis',)


class CVTPulleyDynamicAnalysis(_6001.PulleyDynamicAnalysis):
    '''CVTPulleyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2258.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2258.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
