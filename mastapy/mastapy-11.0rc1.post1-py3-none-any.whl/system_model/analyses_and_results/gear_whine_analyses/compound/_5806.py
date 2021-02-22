'''_5806.py

MountableComponentCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5758
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'MountableComponentCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundGearWhineAnalysis',)


class MountableComponentCompoundGearWhineAnalysis(_5758.ComponentCompoundGearWhineAnalysis):
    '''MountableComponentCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
