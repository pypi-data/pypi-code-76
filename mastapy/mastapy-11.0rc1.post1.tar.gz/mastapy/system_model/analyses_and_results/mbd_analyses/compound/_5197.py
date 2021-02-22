'''_5197.py

BevelGearCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5185
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'BevelGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearCompoundMultibodyDynamicsAnalysis',)


class BevelGearCompoundMultibodyDynamicsAnalysis(_5185.AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis):
    '''BevelGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
