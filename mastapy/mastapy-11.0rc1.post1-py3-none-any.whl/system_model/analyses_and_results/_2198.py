'''_2198.py

AdvancedSystemDeflectionSubAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results import _2196
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'AdvancedSystemDeflectionSubAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionSubAnalysisAnalysis',)


class AdvancedSystemDeflectionSubAnalysisAnalysis(_2196.SingleAnalysis):
    '''AdvancedSystemDeflectionSubAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionSubAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
