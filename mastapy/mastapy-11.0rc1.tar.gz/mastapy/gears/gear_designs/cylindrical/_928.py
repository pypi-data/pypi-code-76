'''_928.py

BacklashSpecification
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _984, _962, _994
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_BACKLASH_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'BacklashSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('BacklashSpecification',)


class BacklashSpecification(_994.RelativeValuesSpecification['BacklashSpecification']):
    '''BacklashSpecification

    This is a mastapy class.
    '''

    TYPE = _BACKLASH_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BacklashSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def left_flank(self) -> '_984.LinearBacklashSepcification':
        '''LinearBacklashSepcification: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_984.LinearBacklashSepcification)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None

    @property
    def right_flank(self) -> '_984.LinearBacklashSepcification':
        '''LinearBacklashSepcification: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_984.LinearBacklashSepcification)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def flanks(self) -> 'List[_984.LinearBacklashSepcification]':
        '''List[LinearBacklashSepcification]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Flanks, constructor.new(_984.LinearBacklashSepcification))
        return value

    @property
    def angular_backlash(self) -> 'List[_962.CylindricalMeshAngularBacklash]':
        '''List[CylindricalMeshAngularBacklash]: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AngularBacklash, constructor.new(_962.CylindricalMeshAngularBacklash))
        return value

    @property
    def both_flanks(self) -> '_984.LinearBacklashSepcification':
        '''LinearBacklashSepcification: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_984.LinearBacklashSepcification)(self.wrapped.BothFlanks) if self.wrapped.BothFlanks else None
