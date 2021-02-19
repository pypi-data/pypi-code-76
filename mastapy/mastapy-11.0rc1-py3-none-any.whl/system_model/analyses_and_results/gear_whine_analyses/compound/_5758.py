'''_5758.py

ComponentCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5808
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ComponentCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundGearWhineAnalysis',)


class ComponentCompoundGearWhineAnalysis(_5808.PartCompoundGearWhineAnalysis):
    '''ComponentCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
