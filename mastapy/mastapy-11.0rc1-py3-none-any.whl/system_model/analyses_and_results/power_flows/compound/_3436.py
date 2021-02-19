'''_3436.py

ConicalGearMeshCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3457
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConicalGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundPowerFlow',)


class ConicalGearMeshCompoundPowerFlow(_3457.GearMeshCompoundPowerFlow):
    '''ConicalGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
