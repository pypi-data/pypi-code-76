'''_4458.py

SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4360
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'SpecialisedAssemblyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundModalAnalysisAtAStiffness',)


class SpecialisedAssemblyCompoundModalAnalysisAtAStiffness(_4360.AbstractAssemblyCompoundModalAnalysisAtAStiffness):
    '''SpecialisedAssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
