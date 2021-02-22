'''_2080.py

CylindricalGearFromCAD
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.import_from_cad import _2086
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'CylindricalGearFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFromCAD',)


class CylindricalGearFromCAD(_2086.MountableComponentFromCAD):
    '''CylindricalGearFromCAD

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_FROM_CAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_teeth(self) -> 'int':
        '''int: 'NumberOfTeeth' is the original name of this property.'''

        return self.wrapped.NumberOfTeeth

    @number_of_teeth.setter
    def number_of_teeth(self, value: 'int'):
        self.wrapped.NumberOfTeeth = int(value) if value else 0

    @property
    def gear_set_name(self) -> 'str':
        '''str: 'GearSetName' is the original name of this property.'''

        return self.wrapped.GearSetName

    @gear_set_name.setter
    def gear_set_name(self, value: 'str'):
        self.wrapped.GearSetName = str(value) if value else None

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.'''

        return self.wrapped.CentreDistance

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def normal_pressure_angle(self) -> 'float':
        '''float: 'NormalPressureAngle' is the original name of this property.'''

        return self.wrapped.NormalPressureAngle

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def normal_module(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NormalModule' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NormalModule) if self.wrapped.NormalModule else None

    @normal_module.setter
    def normal_module(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.NormalModule = value

    @property
    def tip_diameter(self) -> 'float':
        '''float: 'TipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipDiameter

    @property
    def root_diameter(self) -> 'float':
        '''float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootDiameter

    @property
    def cad_drawing_diameter(self) -> 'float':
        '''float: 'CADDrawingDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CADDrawingDiameter
