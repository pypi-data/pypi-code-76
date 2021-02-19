'''_6041.py

GearSetCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6078
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'GearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundDynamicAnalysis',)


class GearSetCompoundDynamicAnalysis(_6078.SpecialisedAssemblyCompoundDynamicAnalysis):
    '''GearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
