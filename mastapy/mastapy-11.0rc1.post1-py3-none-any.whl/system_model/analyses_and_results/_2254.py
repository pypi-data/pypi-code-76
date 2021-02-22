'''_2254.py

CompoundModalAnalysesataSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSESATA_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysesataSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysesataSpeedAnalysis',)


class CompoundModalAnalysesataSpeedAnalysis(_2213.CompoundAnalysis):
    '''CompoundModalAnalysesataSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSESATA_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysesataSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
