'''_3420.py

BevelGearMeshCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3408
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshCompoundPowerFlow',)


class BevelGearMeshCompoundPowerFlow(_3408.AGMAGleasonConicalGearMeshCompoundPowerFlow):
    '''BevelGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
