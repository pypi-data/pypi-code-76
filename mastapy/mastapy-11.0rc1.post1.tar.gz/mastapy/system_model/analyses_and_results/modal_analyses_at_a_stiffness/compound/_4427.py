'''_4427.py

KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4393
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness',)


class KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness(_4393.ConicalGearMeshCompoundModalAnalysisAtAStiffness):
    '''KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
