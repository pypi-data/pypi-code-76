'''_2007.py

ImportedFEWithSelectionComponents
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1073
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.imported_fes import (
    _1996, _1984, _2014, _1976,
    _1975, _2006
)
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
    _1507, _1509, _1508, _1504,
    _1510, _1506, _1505, _1503
)
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WITH_SELECTION_COMPONENTS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEWithSelectionComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWithSelectionComponents',)


class ImportedFEWithSelectionComponents(_2006.ImportedFEWithSelection):
    '''ImportedFEWithSelectionComponents

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WITH_SELECTION_COMPONENTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWithSelectionComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def replace_selected_shaft(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ReplaceSelectedShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReplaceSelectedShaft

    @property
    def auto_select_node_ring(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AutoSelectNodeRing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AutoSelectNodeRing

    @property
    def use_selected_component_for_alignment(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'UseSelectedComponentForAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UseSelectedComponentForAlignment

    @property
    def radius_of_circle_through_selected_nodes(self) -> 'float':
        '''float: 'RadiusOfCircleThroughSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RadiusOfCircleThroughSelectedNodes

    @property
    def manual_alignment(self) -> '_1073.CoordinateSystemEditor':
        '''CoordinateSystemEditor: 'ManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1073.CoordinateSystemEditor)(self.wrapped.ManualAlignment) if self.wrapped.ManualAlignment else None

    @property
    def distance_between_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'DistanceBetweenSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.DistanceBetweenSelectedNodes)
        return value

    @property
    def midpoint_of_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'MidpointOfSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.MidpointOfSelectedNodes)
        return value

    @property
    def centre_of_circle_through_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'CentreOfCircleThroughSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.CentreOfCircleThroughSelectedNodes)
        return value

    @property
    def component_links(self) -> 'List[_1996.ImportedFeLinkWithSelection]':
        '''List[ImportedFeLinkWithSelection]: 'ComponentLinks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentLinks, constructor.new(_1996.ImportedFeLinkWithSelection))
        return value

    @property
    def links_for_selected_component(self) -> 'List[_1996.ImportedFeLinkWithSelection]':
        '''List[ImportedFeLinkWithSelection]: 'LinksForSelectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinksForSelectedComponent, constructor.new(_1996.ImportedFeLinkWithSelection))
        return value

    @property
    def links_for_electric_machine(self) -> 'List[_1996.ImportedFeLinkWithSelection]':
        '''List[ImportedFeLinkWithSelection]: 'LinksForElectricMachine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinksForElectricMachine, constructor.new(_1996.ImportedFeLinkWithSelection))
        return value

    @property
    def rigid_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1507.ElementPropertiesRigid]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesRigid]]: 'RigidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RigidElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1507.ElementPropertiesRigid])
        return value

    @property
    def solid_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1509.ElementPropertiesSolid]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesSolid]]: 'SolidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SolidElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1509.ElementPropertiesSolid])
        return value

    @property
    def shell_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1508.ElementPropertiesShell]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesShell]]: 'ShellElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShellElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1508.ElementPropertiesShell])
        return value

    @property
    def beam_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1504.ElementPropertiesBeam]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesBeam]]: 'BeamElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeamElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1504.ElementPropertiesBeam])
        return value

    @property
    def spring_dashpot_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1510.ElementPropertiesSpringDashpot]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesSpringDashpot]]: 'SpringDashpotElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDashpotElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1510.ElementPropertiesSpringDashpot])
        return value

    @property
    def mass_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1506.ElementPropertiesMass]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesMass]]: 'MassElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1506.ElementPropertiesMass])
        return value

    @property
    def interface_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1505.ElementPropertiesInterface]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesInterface]]: 'InterfaceElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InterfaceElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1505.ElementPropertiesInterface])
        return value

    @property
    def other_element_properties(self) -> 'List[_1984.ElementPropertiesWithSelection[_1503.ElementPropertiesBase]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesBase]]: 'OtherElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OtherElementProperties, constructor.new(_1984.ElementPropertiesWithSelection)[_1503.ElementPropertiesBase])
        return value

    @property
    def materials(self) -> 'List[_2014.MaterialPropertiesWithSelection]':
        '''List[MaterialPropertiesWithSelection]: 'Materials' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Materials, constructor.new(_2014.MaterialPropertiesWithSelection))
        return value

    @property
    def coordinate_systems(self) -> 'List[_1976.CoordinateSystemWithSelection]':
        '''List[CoordinateSystemWithSelection]: 'CoordinateSystems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CoordinateSystems, constructor.new(_1976.CoordinateSystemWithSelection))
        return value

    @property
    def contact_pairs(self) -> 'List[_1975.ContactPairWithSelection]':
        '''List[ContactPairWithSelection]: 'ContactPairs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ContactPairs, constructor.new(_1975.ContactPairWithSelection))
        return value
