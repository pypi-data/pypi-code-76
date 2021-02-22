'''_6325.py

BevelGearMeshCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6313
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BevelGearMeshCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshCompoundCriticalSpeedAnalysis',)


class BevelGearMeshCompoundCriticalSpeedAnalysis(_6313.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis):
    '''BevelGearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
