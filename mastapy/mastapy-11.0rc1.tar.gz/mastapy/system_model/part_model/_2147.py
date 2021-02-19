'''_2147.py

RootAssembly
'''


from typing import List

from mastapy.system_model import _1883
from mastapy._internal import constructor, conversion
from mastapy.geometry import _271
from mastapy.system_model.part_model.projections import _2157
from mastapy.system_model.part_model.part_groups import _2162
from mastapy.system_model.part_model import _2108
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssembly',)


class RootAssembly(_2108.Assembly):
    '''RootAssembly

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def model(self) -> '_1883.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1883.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def packaging_limits(self) -> '_271.PackagingLimits':
        '''PackagingLimits: 'PackagingLimits' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_271.PackagingLimits)(self.wrapped.PackagingLimits) if self.wrapped.PackagingLimits else None

    @property
    def parallel_part_groups_drawing_order(self) -> 'List[_2157.SpecifiedParallelPartGroupDrawingOrder]':
        '''List[SpecifiedParallelPartGroupDrawingOrder]: 'ParallelPartGroupsDrawingOrder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroupsDrawingOrder, constructor.new(_2157.SpecifiedParallelPartGroupDrawingOrder))
        return value

    @property
    def parallel_part_groups(self) -> 'List[_2162.ParallelPartGroup]':
        '''List[ParallelPartGroup]: 'ParallelPartGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroups, constructor.new(_2162.ParallelPartGroup))
        return value

    def attempt_to_fix_all_gear_sets(self):
        ''' 'AttemptToFixAllGearSets' is the original name of this method.'''

        self.wrapped.AttemptToFixAllGearSets()

    def attempt_to_fix_all_cylindrical_gear_sets_by_changing_normal_module(self):
        ''' 'AttemptToFixAllCylindricalGearSetsByChangingNormalModule' is the original name of this method.'''

        self.wrapped.AttemptToFixAllCylindricalGearSetsByChangingNormalModule()

    def open_fe_substructure_version_comparer(self):
        ''' 'OpenFESubstructureVersionComparer' is the original name of this method.'''

        self.wrapped.OpenFESubstructureVersionComparer()
