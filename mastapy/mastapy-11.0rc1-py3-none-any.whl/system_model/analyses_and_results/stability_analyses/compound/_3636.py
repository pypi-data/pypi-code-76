'''_3636.py

PartCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PartCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundStabilityAnalysis',)


class PartCompoundStabilityAnalysis(_7176.PartCompoundAnalysis):
    '''PartCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
