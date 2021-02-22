'''_5420.py

PlanetaryGearSetGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2140
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5363
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PlanetaryGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetGearWhineAnalysis',)


class PlanetaryGearSetGearWhineAnalysis(_5363.CylindricalGearSetGearWhineAnalysis):
    '''PlanetaryGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2140.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
