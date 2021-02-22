'''_6656.py

BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.gears import _2189
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6652
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation',)


class BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation(_6652.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation):
    '''BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2189.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
