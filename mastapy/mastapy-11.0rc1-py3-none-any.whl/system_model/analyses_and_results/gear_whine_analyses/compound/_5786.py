'''_5786.py

GearCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5806
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'GearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundGearWhineAnalysis',)


class GearCompoundGearWhineAnalysis(_5806.MountableComponentCompoundGearWhineAnalysis):
    '''GearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
