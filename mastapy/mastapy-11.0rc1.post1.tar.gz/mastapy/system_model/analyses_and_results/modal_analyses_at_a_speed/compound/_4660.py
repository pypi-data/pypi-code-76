'''_4660.py

CVTPulleyCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4706
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'CVTPulleyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundModalAnalysisAtASpeed',)


class CVTPulleyCompoundModalAnalysisAtASpeed(_4706.PulleyCompoundModalAnalysisAtASpeed):
    '''CVTPulleyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
