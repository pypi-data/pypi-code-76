'''_4230.py

PartCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'PartCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundModalAnalysesAtSpeeds',)


class PartCompoundModalAnalysesAtSpeeds(_6562.PartCompoundAnalysis):
    '''PartCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
