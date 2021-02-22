'''_6263.py

PlanetaryGearSetCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model.gears import _2213
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6228
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'PlanetaryGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCriticalSpeedAnalysis',)


class PlanetaryGearSetCriticalSpeedAnalysis(_6228.CylindricalGearSetCriticalSpeedAnalysis):
    '''PlanetaryGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2213.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
