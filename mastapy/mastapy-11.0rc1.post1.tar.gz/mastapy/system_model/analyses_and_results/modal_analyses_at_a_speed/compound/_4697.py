'''_4697.py

PartCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'PartCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundModalAnalysisAtASpeed',)


class PartCompoundModalAnalysisAtASpeed(_7176.PartCompoundAnalysis):
    '''PartCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
