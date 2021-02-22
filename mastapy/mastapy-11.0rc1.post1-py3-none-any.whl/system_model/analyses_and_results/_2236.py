'''_2236.py

SteadyStateSynchronousResponseonaShaftAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_STEADY_STATE_SYNCHRONOUS_RESPONSEONA_SHAFT_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SteadyStateSynchronousResponseonaShaftAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SteadyStateSynchronousResponseonaShaftAnalysis',)


class SteadyStateSynchronousResponseonaShaftAnalysis(_2214.SingleAnalysis):
    '''SteadyStateSynchronousResponseonaShaftAnalysis

    This is a mastapy class.
    '''

    TYPE = _STEADY_STATE_SYNCHRONOUS_RESPONSEONA_SHAFT_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SteadyStateSynchronousResponseonaShaftAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
