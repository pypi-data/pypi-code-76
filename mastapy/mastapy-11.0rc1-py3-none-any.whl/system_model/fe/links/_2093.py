'''_2093.py

FELinkWithSelection
'''


from mastapy.system_model.fe.links import (
    _2091, _2092, _2094, _2095,
    _2096, _2097, _2098, _2099,
    _2100, _2101, _2102, _2103,
    _2104, _2105
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_LINK_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'FELinkWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FELinkWithSelection',)


class FELinkWithSelection(_0.APIBase):
    '''FELinkWithSelection

    This is a mastapy class.
    '''

    TYPE = _FE_LINK_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FELinkWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def link(self) -> '_2091.FELink':
        '''FELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.FELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to FELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_electric_machine_stator_fe_link(self) -> '_2092.ElectricMachineStatorFELink':
        '''ElectricMachineStatorFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.ElectricMachineStatorFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ElectricMachineStatorFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_gear_mesh_fe_link(self) -> '_2094.GearMeshFELink':
        '''GearMeshFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.GearMeshFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to GearMeshFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_gear_with_duplicated_meshes_fe_link(self) -> '_2095.GearWithDuplicatedMeshesFELink':
        '''GearWithDuplicatedMeshesFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.GearWithDuplicatedMeshesFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to GearWithDuplicatedMeshesFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_angle_connection_fe_link(self) -> '_2096.MultiAngleConnectionFELink':
        '''MultiAngleConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.MultiAngleConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiAngleConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_node_connector_fe_link(self) -> '_2097.MultiNodeConnectorFELink':
        '''MultiNodeConnectorFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.MultiNodeConnectorFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiNodeConnectorFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_node_fe_link(self) -> '_2098.MultiNodeFELink':
        '''MultiNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.MultiNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiNodeFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planetary_connector_multi_node_fe_link(self) -> '_2099.PlanetaryConnectorMultiNodeFELink':
        '''PlanetaryConnectorMultiNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.PlanetaryConnectorMultiNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetaryConnectorMultiNodeFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planet_based_fe_link(self) -> '_2100.PlanetBasedFELink':
        '''PlanetBasedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PlanetBasedFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetBasedFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planet_carrier_fe_link(self) -> '_2101.PlanetCarrierFELink':
        '''PlanetCarrierFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.PlanetCarrierFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetCarrierFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_point_load_fe_link(self) -> '_2102.PointLoadFELink':
        '''PointLoadFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2102.PointLoadFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PointLoadFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_fe_link(self) -> '_2103.RollingRingConnectionFELink':
        '''RollingRingConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2103.RollingRingConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to RollingRingConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_2104.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2104.ShaftHubConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_single_node_fe_link(self) -> '_2105.SingleNodeFELink':
        '''SingleNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2105.SingleNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to SingleNodeFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    def add_selected_nodes(self):
        ''' 'AddSelectedNodes' is the original name of this method.'''

        self.wrapped.AddSelectedNodes()

    def delete_all_nodes(self):
        ''' 'DeleteAllNodes' is the original name of this method.'''

        self.wrapped.DeleteAllNodes()

    def select_component(self):
        ''' 'SelectComponent' is the original name of this method.'''

        self.wrapped.SelectComponent()
