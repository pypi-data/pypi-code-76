'''_5808.py

PartCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PartCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundGearWhineAnalysis',)


class PartCompoundGearWhineAnalysis(_6562.PartCompoundAnalysis):
    '''PartCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
