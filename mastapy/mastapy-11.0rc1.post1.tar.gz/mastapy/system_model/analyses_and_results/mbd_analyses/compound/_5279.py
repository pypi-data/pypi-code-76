'''_5279.py

SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5181
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis',)


class SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis(_5181.AbstractAssemblyCompoundMultibodyDynamicsAnalysis):
    '''SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
