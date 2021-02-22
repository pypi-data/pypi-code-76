'''_2264.py

CompoundSteadyStateSynchronousResponseataSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSEATA_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSteadyStateSynchronousResponseataSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSteadyStateSynchronousResponseataSpeedAnalysis',)


class CompoundSteadyStateSynchronousResponseataSpeedAnalysis(_2213.CompoundAnalysis):
    '''CompoundSteadyStateSynchronousResponseataSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSEATA_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSteadyStateSynchronousResponseataSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
