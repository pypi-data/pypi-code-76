'''_5222.py

CVTCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5191
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CVTCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundMultibodyDynamicsAnalysis',)


class CVTCompoundMultibodyDynamicsAnalysis(_5191.BeltDriveCompoundMultibodyDynamicsAnalysis):
    '''CVTCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
