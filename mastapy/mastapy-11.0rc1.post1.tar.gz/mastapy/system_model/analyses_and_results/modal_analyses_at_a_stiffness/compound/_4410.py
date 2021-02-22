'''_4410.py

CylindricalPlanetGearCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4407
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CylindricalPlanetGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundModalAnalysisAtAStiffness',)


class CylindricalPlanetGearCompoundModalAnalysisAtAStiffness(_4407.CylindricalGearCompoundModalAnalysisAtAStiffness):
    '''CylindricalPlanetGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
