'''_5677.py

HypoidGearMeshHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1991
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6536
from mastapy.system_model.analyses_and_results.system_deflections import _2425
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5595
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HypoidGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshHarmonicAnalysis',)


class HypoidGearMeshHarmonicAnalysis(_5595.AGMAGleasonConicalGearMeshHarmonicAnalysis):
    '''HypoidGearMeshHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1991.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6536.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6536.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2425.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2425.HypoidGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
