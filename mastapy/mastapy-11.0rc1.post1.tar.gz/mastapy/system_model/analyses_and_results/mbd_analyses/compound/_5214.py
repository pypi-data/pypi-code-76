'''_5214.py

ConicalGearMeshCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5240
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ConicalGearMeshCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundMultibodyDynamicsAnalysis',)


class ConicalGearMeshCompoundMultibodyDynamicsAnalysis(_5240.GearMeshCompoundMultibodyDynamicsAnalysis):
    '''ConicalGearMeshCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[ConicalGearMeshCompoundMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundMultibodyDynamicsAnalysis))
        return value
