'''_5849.py

VirtualComponentCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5806
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'VirtualComponentCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundGearWhineAnalysis',)


class VirtualComponentCompoundGearWhineAnalysis(_5806.MountableComponentCompoundGearWhineAnalysis):
    '''VirtualComponentCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
