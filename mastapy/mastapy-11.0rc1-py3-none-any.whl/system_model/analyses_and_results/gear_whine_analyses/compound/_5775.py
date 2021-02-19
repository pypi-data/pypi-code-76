'''_5775.py

CVTPulleyCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5817
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CVTPulleyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundGearWhineAnalysis',)


class CVTPulleyCompoundGearWhineAnalysis(_5817.PulleyCompoundGearWhineAnalysis):
    '''CVTPulleyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
