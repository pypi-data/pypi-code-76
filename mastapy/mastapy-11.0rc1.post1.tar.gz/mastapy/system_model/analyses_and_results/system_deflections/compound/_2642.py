'''_2642.py

ZerolBevelGearMeshCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2501
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2530
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ZerolBevelGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundSystemDeflection',)


class ZerolBevelGearMeshCompoundSystemDeflection(_2530.BevelGearMeshCompoundSystemDeflection):
    '''ZerolBevelGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2501.ZerolBevelGearMeshSystemDeflection]':
        '''List[ZerolBevelGearMeshSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2501.ZerolBevelGearMeshSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2501.ZerolBevelGearMeshSystemDeflection]':
        '''List[ZerolBevelGearMeshSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2501.ZerolBevelGearMeshSystemDeflection))
        return value
