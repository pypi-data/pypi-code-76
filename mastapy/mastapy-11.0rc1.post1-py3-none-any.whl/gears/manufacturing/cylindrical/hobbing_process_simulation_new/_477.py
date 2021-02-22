'''_477.py

WormGrindingProcessGearShape
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _476
from mastapy._internal.python_net import python_net_import

_WORM_GRINDING_PROCESS_GEAR_SHAPE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'WormGrindingProcessGearShape')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrindingProcessGearShape',)


class WormGrindingProcessGearShape(_476.WormGrindingProcessCalculation):
    '''WormGrindingProcessGearShape

    This is a mastapy class.
    '''

    TYPE = _WORM_GRINDING_PROCESS_GEAR_SHAPE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGrindingProcessGearShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def result_z_plane(self) -> 'float':
        '''float: 'ResultZPlane' is the original name of this property.'''

        return self.wrapped.ResultZPlane

    @result_z_plane.setter
    def result_z_plane(self, value: 'float'):
        self.wrapped.ResultZPlane = float(value) if value else 0.0

    @property
    def number_of_gear_shape_bands(self) -> 'int':
        '''int: 'NumberOfGearShapeBands' is the original name of this property.'''

        return self.wrapped.NumberOfGearShapeBands

    @number_of_gear_shape_bands.setter
    def number_of_gear_shape_bands(self, value: 'int'):
        self.wrapped.NumberOfGearShapeBands = int(value) if value else 0
