'''_6028.py

CVTPulleyCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6070
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CVTPulleyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundDynamicAnalysis',)


class CVTPulleyCompoundDynamicAnalysis(_6070.PulleyCompoundDynamicAnalysis):
    '''CVTPulleyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
