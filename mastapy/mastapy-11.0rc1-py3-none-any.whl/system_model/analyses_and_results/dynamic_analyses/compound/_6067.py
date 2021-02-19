'''_6067.py

ComponentCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6121
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ComponentCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundDynamicAnalysis',)


class ComponentCompoundDynamicAnalysis(_6121.PartCompoundDynamicAnalysis):
    '''ComponentCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
