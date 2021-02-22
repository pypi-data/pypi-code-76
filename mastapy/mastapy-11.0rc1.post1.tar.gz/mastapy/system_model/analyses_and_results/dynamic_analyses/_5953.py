'''_5953.py

CVTDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2257
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5922
from mastapy._internal.python_net import python_net_import

_CVT_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CVTDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTDynamicAnalysis',)


class CVTDynamicAnalysis(_5922.BeltDriveDynamicAnalysis):
    '''CVTDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2257.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2257.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
