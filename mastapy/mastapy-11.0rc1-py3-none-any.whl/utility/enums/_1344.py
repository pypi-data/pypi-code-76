'''_1344.py

ThreeDViewContourOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_THREE_D_VIEW_CONTOUR_OPTION = python_net_import('SMT.MastaAPI.Utility.Enums', 'ThreeDViewContourOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreeDViewContourOption',)


class ThreeDViewContourOption(Enum):
    '''ThreeDViewContourOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _THREE_D_VIEW_CONTOUR_OPTION

    __hash__ = None

    NO_CONTOUR = 0
    STRAIN_ENERGY_PER_COMPONENT = 1
    KINETIC_ENERGY_PER_COMPONENT = 2
    STRAIN_ENERGY_PER_ELEMENT = 3
    KINETIC_ENERGY_PER_ELEMENT = 4
    DISPLACEMENT_ANGULAR_MAGNITUDE = 5
    DISPLACEMENT_RADIAL_TILT_MAGNITUDE = 6
    DISPLACEMENT_TWIST = 7
    DISPLACEMENT_LINEAR_MAGNITUDE = 8
    DISPLACEMENT_RADIAL_MAGNITUDE = 9
    DISPLACEMENT_AXIAL = 10
    FORCE_ANGULAR_MAGNITUDE = 11
    FORCE_TORQUE = 12
    FORCE_LINEAR_MAGNITUDE = 13
    FORCE_RADIAL_MAGNITUDE = 14
    FORCE_AXIAL = 15
    STRESS_NOMINAL_AXIAL = 16
    STRESS_NOMINAL_BENDING = 17
    STRESS_NOMINAL_TORSIONAL = 18
    STRESS_NOMINAL_VON_MISES_ALTERNATING = 19
    STRESS_NOMINAL_VON_MISES_MAX = 20
    STRESS_NOMINAL_VON_MISES_MEAN = 21
    STRESS_NOMINAL_MAXIMUM_PRINCIPAL = 22
    STRESS_NOMINAL_MINIMUM_PRINCIPAL = 23
    FE_MESH_NORMAL_DISPLACEMENT = 24
    FE_MESH_NORMAL_VELOCITY = 25
    FE_MESH_NORMAL_ACCELERATION = 26


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


ThreeDViewContourOption.__setattr__ = __enum_setattr
ThreeDViewContourOption.__delattr__ = __enum_delattr
