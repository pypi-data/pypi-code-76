'''_5774.py

CVTCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5743
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CVTCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundGearWhineAnalysis',)


class CVTCompoundGearWhineAnalysis(_5743.BeltDriveCompoundGearWhineAnalysis):
    '''CVTCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
