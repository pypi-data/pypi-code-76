'''_1004.py

SplineMaterial
'''


from mastapy.detailed_rigid_connectors.splines import _986
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.materials import _73
from mastapy._internal.python_net import python_net_import

_SPLINE_MATERIAL = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineMaterial',)


class SplineMaterial(_73.Material):
    '''SplineMaterial

    This is a mastapy class.
    '''

    TYPE = _SPLINE_MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SplineMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def heat_treatment_type(self) -> '_986.HeatTreatmentTypes':
        '''HeatTreatmentTypes: 'HeatTreatmentType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HeatTreatmentType)
        return constructor.new(_986.HeatTreatmentTypes)(value) if value else None

    @heat_treatment_type.setter
    def heat_treatment_type(self, value: '_986.HeatTreatmentTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HeatTreatmentType = value

    @property
    def core_hardness_h_rc(self) -> 'float':
        '''float: 'CoreHardnessHRc' is the original name of this property.'''

        return self.wrapped.CoreHardnessHRc

    @core_hardness_h_rc.setter
    def core_hardness_h_rc(self, value: 'float'):
        self.wrapped.CoreHardnessHRc = float(value) if value else 0.0
