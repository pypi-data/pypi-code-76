'''_5557.py

PlanetaryGearSetSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2140
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5520
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PlanetaryGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetSingleMeshWhineAnalysis',)


class PlanetaryGearSetSingleMeshWhineAnalysis(_5520.CylindricalGearSetSingleMeshWhineAnalysis):
    '''PlanetaryGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2140.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
