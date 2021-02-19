'''_320.py

GearMeshRating
'''


from mastapy._internal import constructor
from mastapy.gears.load_case import _810
from mastapy.gears.load_case.worm import _813
from mastapy._internal.cast_exception import CastException
from mastapy.gears.load_case.face import _816
from mastapy.gears.load_case.cylindrical import _819
from mastapy.gears.load_case.conical import _822
from mastapy.gears.load_case.concept import _825
from mastapy.gears.load_case.bevel import _827
from mastapy.gears.rating import _313
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshRating',)


class GearMeshRating(_313.AbstractGearMeshRating):
    '''GearMeshRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_energy(self) -> 'float':
        '''float: 'TotalEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalEnergy

    @property
    def energy_loss(self) -> 'float':
        '''float: 'EnergyLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EnergyLoss

    @property
    def pinion_name(self) -> 'str':
        '''str: 'PinionName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionName

    @property
    def wheel_name(self) -> 'str':
        '''str: 'WheelName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelName

    @property
    def signed_pinion_torque(self) -> 'float':
        '''float: 'SignedPinionTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedPinionTorque

    @property
    def signed_wheel_torque(self) -> 'float':
        '''float: 'SignedWheelTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedWheelTorque

    @property
    def pinion_torque(self) -> 'float':
        '''float: 'PinionTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionTorque

    @property
    def wheel_torque(self) -> 'float':
        '''float: 'WheelTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelTorque

    @property
    def driving_gear(self) -> 'str':
        '''str: 'DrivingGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DrivingGear

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def mesh_efficiency(self) -> 'float':
        '''float: 'MeshEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshEfficiency

    @property
    def mesh_load_case(self) -> '_810.MeshLoadCase':
        '''MeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _810.MeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to MeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_worm_mesh_load_case(self) -> '_813.WormMeshLoadCase':
        '''WormMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _813.WormMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to WormMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_face_mesh_load_case(self) -> '_816.FaceMeshLoadCase':
        '''FaceMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _816.FaceMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to FaceMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_cylindrical_mesh_load_case(self) -> '_819.CylindricalMeshLoadCase':
        '''CylindricalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _819.CylindricalMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to CylindricalMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_conical_mesh_load_case(self) -> '_822.ConicalMeshLoadCase':
        '''ConicalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _822.ConicalMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to ConicalMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_concept_mesh_load_case(self) -> '_825.ConceptMeshLoadCase':
        '''ConceptMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _825.ConceptMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to ConceptMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def mesh_load_case_of_type_bevel_mesh_load_case(self) -> '_827.BevelMeshLoadCase':
        '''BevelMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _827.BevelMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to BevelMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None
