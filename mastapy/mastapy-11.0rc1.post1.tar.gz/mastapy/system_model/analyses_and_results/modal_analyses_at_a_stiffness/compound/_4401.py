'''_4401.py

CVTCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4370
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CVTCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundModalAnalysisAtAStiffness',)


class CVTCompoundModalAnalysisAtAStiffness(_4370.BeltDriveCompoundModalAnalysisAtAStiffness):
    '''CVTCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
