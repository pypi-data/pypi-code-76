'''_4378.py

BevelGearSetCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4366
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'BevelGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetCompoundModalAnalysisAtAStiffness',)


class BevelGearSetCompoundModalAnalysisAtAStiffness(_4366.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness):
    '''BevelGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
