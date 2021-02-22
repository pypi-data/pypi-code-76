'''_6387.py

PartCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'PartCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundCriticalSpeedAnalysis',)


class PartCompoundCriticalSpeedAnalysis(_7176.PartCompoundAnalysis):
    '''PartCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
