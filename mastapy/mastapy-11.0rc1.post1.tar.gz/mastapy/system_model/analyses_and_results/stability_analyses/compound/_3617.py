'''_3617.py

GearSetCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3655
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'GearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundStabilityAnalysis',)


class GearSetCompoundStabilityAnalysis(_3655.SpecialisedAssemblyCompoundStabilityAnalysis):
    '''GearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
