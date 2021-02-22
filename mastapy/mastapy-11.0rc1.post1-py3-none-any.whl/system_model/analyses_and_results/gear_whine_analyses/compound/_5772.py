'''_5772.py

CouplingHalfCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5806
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CouplingHalfCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundGearWhineAnalysis',)


class CouplingHalfCompoundGearWhineAnalysis(_5806.MountableComponentCompoundGearWhineAnalysis):
    '''CouplingHalfCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
