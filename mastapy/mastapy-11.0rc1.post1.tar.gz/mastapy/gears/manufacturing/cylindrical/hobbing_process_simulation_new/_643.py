'''_643.py

WormGrindingProcessPitchCalculation
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _607, _640
from mastapy._internal.python_net import python_net_import

_WORM_GRINDING_PROCESS_PITCH_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'WormGrindingProcessPitchCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrindingProcessPitchCalculation',)


class WormGrindingProcessPitchCalculation(_640.WormGrindingProcessCalculation):
    '''WormGrindingProcessPitchCalculation

    This is a mastapy class.
    '''

    TYPE = _WORM_GRINDING_PROCESS_PITCH_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGrindingProcessPitchCalculation.TYPE'):
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
    def right_flank(self) -> '_607.CalculatePitchDeviationAccuracy':
        '''CalculatePitchDeviationAccuracy: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_607.CalculatePitchDeviationAccuracy)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def left_flank(self) -> '_607.CalculatePitchDeviationAccuracy':
        '''CalculatePitchDeviationAccuracy: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_607.CalculatePitchDeviationAccuracy)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None
