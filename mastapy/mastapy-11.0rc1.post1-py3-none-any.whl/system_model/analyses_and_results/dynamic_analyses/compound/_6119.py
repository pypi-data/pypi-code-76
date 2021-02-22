'''_6119.py

MountableComponentCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6067
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'MountableComponentCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundDynamicAnalysis',)


class MountableComponentCompoundDynamicAnalysis(_6067.ComponentCompoundDynamicAnalysis):
    '''MountableComponentCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
