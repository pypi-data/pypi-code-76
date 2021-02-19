'''_6471.py

ConceptCouplingLoadCase
'''


from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model import _1886
from mastapy.system_model.part_model import _2145
from mastapy.system_model.part_model.couplings import _2252
from mastapy.math_utility.control import _1334
from mastapy.system_model.analyses_and_results.static_loads import _6484
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingLoadCase',)


class ConceptCouplingLoadCase(_6484.CouplingLoadCase):
    '''ConceptCouplingLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def speed_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedRatio) if self.wrapped.SpeedRatio else None

    @speed_ratio.setter
    def speed_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpeedRatio = value

    @property
    def efficiency(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Efficiency' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Efficiency) if self.wrapped.Efficiency else None

    @efficiency.setter
    def efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Efficiency = value

    @property
    def speed_ratio_specification_method(self) -> '_1886.ConceptCouplingSpeedRatioSpecificationMethod':
        '''ConceptCouplingSpeedRatioSpecificationMethod: 'SpeedRatioSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpeedRatioSpecificationMethod)
        return constructor.new(_1886.ConceptCouplingSpeedRatioSpecificationMethod)(value) if value else None

    @speed_ratio_specification_method.setter
    def speed_ratio_specification_method(self, value: '_1886.ConceptCouplingSpeedRatioSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpeedRatioSpecificationMethod = value

    @property
    def power_load_for_reference_speed(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'PowerLoadForReferenceSpeed' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.PowerLoadForReferenceSpeed) if self.wrapped.PowerLoadForReferenceSpeed else None

    @power_load_for_reference_speed.setter
    def power_load_for_reference_speed(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.PowerLoadForReferenceSpeed = value

    @property
    def assembly_design(self) -> '_2252.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def speed_ratio_pid_control(self) -> '_1334.PIDControlSettings':
        '''PIDControlSettings: 'SpeedRatioPIDControl' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1334.PIDControlSettings)(self.wrapped.SpeedRatioPIDControl) if self.wrapped.SpeedRatioPIDControl else None
