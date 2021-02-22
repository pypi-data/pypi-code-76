'''_6691.py

CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6688
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation',)


class CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation(_6688.CylindricalGearAdvancedTimeSteppingAnalysisForModulation):
    '''CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2198.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
