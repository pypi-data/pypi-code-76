'''_6367.py

GearMeshCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6373
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'GearMeshCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundCriticalSpeedAnalysis',)


class GearMeshCompoundCriticalSpeedAnalysis(_6373.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis):
    '''GearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
