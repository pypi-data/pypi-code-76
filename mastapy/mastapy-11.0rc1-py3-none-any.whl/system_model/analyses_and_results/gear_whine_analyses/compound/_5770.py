'''_5770.py

CouplingCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5825
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CouplingCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundGearWhineAnalysis',)


class CouplingCompoundGearWhineAnalysis(_5825.SpecialisedAssemblyCompoundGearWhineAnalysis):
    '''CouplingCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
