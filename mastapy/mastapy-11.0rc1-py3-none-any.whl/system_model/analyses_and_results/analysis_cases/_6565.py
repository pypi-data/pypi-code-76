'''_6565.py

PartTimeSeriesLoadAnalysisCase
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6561
from mastapy._internal.python_net import python_net_import

_PART_TIME_SERIES_LOAD_ANALYSIS_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'PartTimeSeriesLoadAnalysisCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PartTimeSeriesLoadAnalysisCase',)


class PartTimeSeriesLoadAnalysisCase(_6561.PartAnalysisCase):
    '''PartTimeSeriesLoadAnalysisCase

    This is a mastapy class.
    '''

    TYPE = _PART_TIME_SERIES_LOAD_ANALYSIS_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartTimeSeriesLoadAnalysisCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
