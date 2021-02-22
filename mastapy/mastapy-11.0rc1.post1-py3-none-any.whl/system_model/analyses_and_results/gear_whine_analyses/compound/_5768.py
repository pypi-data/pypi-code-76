'''_5768.py

ConnectionCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6555
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundGearWhineAnalysis',)


class ConnectionCompoundGearWhineAnalysis(_6555.ConnectionCompoundAnalysis):
    '''ConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
