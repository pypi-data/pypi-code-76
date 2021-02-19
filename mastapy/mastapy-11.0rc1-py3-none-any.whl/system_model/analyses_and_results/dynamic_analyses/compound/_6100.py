'''_6100.py

GearCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6119
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'GearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundDynamicAnalysis',)


class GearCompoundDynamicAnalysis(_6119.MountableComponentCompoundDynamicAnalysis):
    '''GearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
