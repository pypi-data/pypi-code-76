'''_6121.py

PartCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PartCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundDynamicAnalysis',)


class PartCompoundDynamicAnalysis(_7176.PartCompoundAnalysis):
    '''PartCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
