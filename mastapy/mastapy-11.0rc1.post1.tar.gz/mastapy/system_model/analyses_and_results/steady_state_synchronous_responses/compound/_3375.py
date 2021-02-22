'''_3375.py

PartCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'PartCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundSteadyStateSynchronousResponse',)


class PartCompoundSteadyStateSynchronousResponse(_7176.PartCompoundAnalysis):
    '''PartCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
