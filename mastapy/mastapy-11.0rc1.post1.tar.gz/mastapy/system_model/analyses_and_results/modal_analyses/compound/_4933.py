'''_4933.py

ConicalGearMeshCompoundModalAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4959
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConicalGearMeshCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundModalAnalysis',)


class ConicalGearMeshCompoundModalAnalysis(_4959.GearMeshCompoundModalAnalysis):
    '''ConicalGearMeshCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundModalAnalysis]':
        '''List[ConicalGearMeshCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundModalAnalysis))
        return value
