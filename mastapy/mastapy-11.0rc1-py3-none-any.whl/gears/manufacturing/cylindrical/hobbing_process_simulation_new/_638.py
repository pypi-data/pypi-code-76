'''_638.py

WormGrindingCutterCalculation
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _599
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _640
from mastapy._internal.python_net import python_net_import

_WORM_GRINDING_CUTTER_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'WormGrindingCutterCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrindingCutterCalculation',)


class WormGrindingCutterCalculation(_640.WormGrindingProcessCalculation):
    '''WormGrindingCutterCalculation

    This is a mastapy class.
    '''

    TYPE = _WORM_GRINDING_CUTTER_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGrindingCutterCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_profile_bands(self) -> 'int':
        '''int: 'NumberOfProfileBands' is the original name of this property.'''

        return self.wrapped.NumberOfProfileBands

    @number_of_profile_bands.setter
    def number_of_profile_bands(self, value: 'int'):
        self.wrapped.NumberOfProfileBands = int(value) if value else 0

    @property
    def use_design_mode_micro_geometry(self) -> 'bool':
        '''bool: 'UseDesignModeMicroGeometry' is the original name of this property.'''

        return self.wrapped.UseDesignModeMicroGeometry

    @use_design_mode_micro_geometry.setter
    def use_design_mode_micro_geometry(self, value: 'bool'):
        self.wrapped.UseDesignModeMicroGeometry = bool(value) if value else False

    @property
    def worm_radius(self) -> 'float':
        '''float: 'WormRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WormRadius

    @property
    def worm_axial_z(self) -> 'float':
        '''float: 'WormAxialZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WormAxialZ

    @property
    def input_gear_point_of_interest(self) -> '_599.PointOfInterest':
        '''PointOfInterest: 'InputGearPointOfInterest' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_599.PointOfInterest)(self.wrapped.InputGearPointOfInterest) if self.wrapped.InputGearPointOfInterest else None

    def calculate_grinder_axial_section_tooth_shape(self):
        ''' 'CalculateGrinderAxialSectionToothShape' is the original name of this method.'''

        self.wrapped.CalculateGrinderAxialSectionToothShape()

    def calculate_point_of_interest(self):
        ''' 'CalculatePointOfInterest' is the original name of this method.'''

        self.wrapped.CalculatePointOfInterest()
