'''_2501.py

ZerolBevelGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6618
from mastapy.system_model.analyses_and_results.power_flows import _3822
from mastapy.gears.rating.zerol_bevel import _329
from mastapy.system_model.analyses_and_results.system_deflections import _2370
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ZerolBevelGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshSystemDeflection',)


class ZerolBevelGearMeshSystemDeflection(_2370.BevelGearMeshSystemDeflection):
    '''ZerolBevelGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6618.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6618.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3822.ZerolBevelGearMeshPowerFlow':
        '''ZerolBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3822.ZerolBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_329.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_329.ZerolBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_329.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_329.ZerolBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
