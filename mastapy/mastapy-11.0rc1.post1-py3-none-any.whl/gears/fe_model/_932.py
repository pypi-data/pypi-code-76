'''_932.py

GearFEModel
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.fe_model import _934
from mastapy.gears import _126
from mastapy import _6531
from mastapy._internal.python_net import python_net_import
from mastapy.gears.analysis import _953

_GEAR_FLANKS = python_net_import('SMT.MastaAPI.Gears', 'GearFlanks')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_GEAR_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearFEModel',)


class GearFEModel(_953.GearImplementationDetail):
    '''GearFEModel

    This is a mastapy class.
    '''

    TYPE = _GEAR_FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_all_teeth_in_the_fe_mesh(self) -> 'bool':
        '''bool: 'IncludeAllTeethInTheFEMesh' is the original name of this property.'''

        return self.wrapped.IncludeAllTeethInTheFEMesh

    @include_all_teeth_in_the_fe_mesh.setter
    def include_all_teeth_in_the_fe_mesh(self, value: 'bool'):
        self.wrapped.IncludeAllTeethInTheFEMesh = bool(value) if value else False

    @property
    def fe_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FEBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FEBore) if self.wrapped.FEBore else None

    @fe_bore.setter
    def fe_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.FEBore = value

    @property
    def element_settings(self) -> '_934.GearMeshingElementOptions':
        '''GearMeshingElementOptions: 'ElementSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_934.GearMeshingElementOptions)(self.wrapped.ElementSettings) if self.wrapped.ElementSettings else None

    def get_stress_influence_coefficients_from_fe(self, flank: '_126.GearFlanks'):
        ''' 'GetStressInfluenceCoefficientsFromFE' is the original name of this method.

        Args:
            flank (mastapy.gears.GearFlanks)
        '''

        flank = conversion.mp_to_pn_enum(flank)
        self.wrapped.GetStressInfluenceCoefficientsFromFE.Overloads[_GEAR_FLANKS](flank)

    def get_stress_influence_coefficients_from_fe_with_progress(self, flank: '_126.GearFlanks', progress: '_6531.TaskProgress'):
        ''' 'GetStressInfluenceCoefficientsFromFE' is the original name of this method.

        Args:
            flank (mastapy.gears.GearFlanks)
            progress (mastapy.TaskProgress)
        '''

        flank = conversion.mp_to_pn_enum(flank)
        self.wrapped.GetStressInfluenceCoefficientsFromFE.Overloads[_GEAR_FLANKS, _TASK_PROGRESS](flank, progress.wrapped if progress else None)

    def calculate_stiffness_from_fe(self):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.'''

        self.wrapped.CalculateStiffnessFromFE()

    def calculate_stiffness_from_fe_with_progress(self, progress: '_6531.TaskProgress'):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        '''

        self.wrapped.CalculateStiffnessFromFE.Overloads[_TASK_PROGRESS](progress.wrapped if progress else None)
