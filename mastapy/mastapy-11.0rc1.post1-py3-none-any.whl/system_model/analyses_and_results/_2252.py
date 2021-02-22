'''_2252.py

CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODELFOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis',)


class CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis(_2213.CompoundAnalysis):
    '''CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_MODELFOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
