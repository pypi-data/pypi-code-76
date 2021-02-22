'''_4420.py

GearSetCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4458
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'GearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundModalAnalysisAtAStiffness',)


class GearSetCompoundModalAnalysisAtAStiffness(_4458.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness):
    '''GearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
