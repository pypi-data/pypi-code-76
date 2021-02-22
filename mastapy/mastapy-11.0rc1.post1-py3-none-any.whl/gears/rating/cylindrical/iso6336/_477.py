'''_477.py

ISO6336RateableMesh
'''


from mastapy.gears.rating.cylindrical import _434, _427
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import

_ISO6336_RATEABLE_MESH = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336RateableMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336RateableMesh',)


class ISO6336RateableMesh(_427.CylindricalRateableMesh):
    '''ISO6336RateableMesh

    This is a mastapy class.
    '''

    TYPE = _ISO6336_RATEABLE_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO6336RateableMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def misalignment_contact_pattern_enhancement(self) -> '_434.MisalignmentContactPatternEnhancements':
        '''MisalignmentContactPatternEnhancements: 'MisalignmentContactPatternEnhancement' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MisalignmentContactPatternEnhancement)
        return constructor.new(_434.MisalignmentContactPatternEnhancements)(value) if value else None

    @misalignment_contact_pattern_enhancement.setter
    def misalignment_contact_pattern_enhancement(self, value: '_434.MisalignmentContactPatternEnhancements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MisalignmentContactPatternEnhancement = value
