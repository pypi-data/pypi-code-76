'''_949.py

CylindricalGearMeshFlankDesign
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_FLANK_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearMeshFlankDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshFlankDesign',)


class CylindricalGearMeshFlankDesign(_0.APIBase):
    '''CylindricalGearMeshFlankDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_FLANK_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshFlankDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def working_transverse_pressure_angle(self) -> 'float':
        '''float: 'WorkingTransversePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorkingTransversePressureAngle

    @property
    def working_normal_pressure_angle(self) -> 'float':
        '''float: 'WorkingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorkingNormalPressureAngle

    @property
    def virtual_contact_ratio(self) -> 'float':
        '''float: 'VirtualContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VirtualContactRatio

    @property
    def total_contact_ratio(self) -> 'float':
        '''float: 'TotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalContactRatio

    @property
    def transverse_contact_ratio(self) -> 'float':
        '''float: 'TransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatio

    @property
    def length_of_contact(self) -> 'float':
        '''float: 'LengthOfContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthOfContact

    @property
    def tooth_loss_factor(self) -> 'float':
        '''float: 'ToothLossFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothLossFactor

    @property
    def degree_of_tooth_loss(self) -> 'float':
        '''float: 'DegreeOfToothLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DegreeOfToothLoss

    @property
    def flank_name(self) -> 'str':
        '''str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FlankName
