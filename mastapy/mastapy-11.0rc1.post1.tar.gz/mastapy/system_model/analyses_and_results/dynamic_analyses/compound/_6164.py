'''_6164.py

VirtualComponentCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6119
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'VirtualComponentCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundDynamicAnalysis',)


class VirtualComponentCompoundDynamicAnalysis(_6119.MountableComponentCompoundDynamicAnalysis):
    '''VirtualComponentCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
