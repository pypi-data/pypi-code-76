'''_4950.py

CylindricalPlanetGearCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4947
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CylindricalPlanetGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundModalAnalysis',)


class CylindricalPlanetGearCompoundModalAnalysis(_4947.CylindricalGearCompoundModalAnalysis):
    '''CylindricalPlanetGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
