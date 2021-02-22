'''_2247.py

CompoundAdvancedSystemDeflectionSubAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundAdvancedSystemDeflectionSubAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundAdvancedSystemDeflectionSubAnalysisAnalysis',)


class CompoundAdvancedSystemDeflectionSubAnalysisAnalysis(_2213.CompoundAnalysis):
    '''CompoundAdvancedSystemDeflectionSubAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundAdvancedSystemDeflectionSubAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
