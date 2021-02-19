'''_2069.py

FELinkWithSelection
'''


from mastapy.system_model.fe.links import (
    _2067, _2068, _2070, _2071,
    _2072, _2073, _2074, _2075,
    _2076, _2077, _2078, _2079,
    _2080, _2081
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
    def link(self) -> '_2067.FELink':
        '''FELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.FELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to FELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_electric_machine_stator_fe_link(self) -> '_2068.ElectricMachineStatorFELink':
        '''ElectricMachineStatorFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.ElectricMachineStatorFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ElectricMachineStatorFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_gear_mesh_fe_link(self) -> '_2070.GearMeshFELink':
        '''GearMeshFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.GearMeshFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to GearMeshFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_gear_with_duplicated_meshes_fe_link(self) -> '_2071.GearWithDuplicatedMeshesFELink':
        '''GearWithDuplicatedMeshesFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.GearWithDuplicatedMeshesFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to GearWithDuplicatedMeshesFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_angle_connection_fe_link(self) -> '_2072.MultiAngleConnectionFELink':
        '''MultiAngleConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.MultiAngleConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiAngleConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_node_connector_fe_link(self) -> '_2073.MultiNodeConnectorFELink':
        '''MultiNodeConnectorFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.MultiNodeConnectorFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiNodeConnectorFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_node_fe_link(self) -> '_2074.MultiNodeFELink':
        '''MultiNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.MultiNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiNodeFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planetary_connector_multi_node_fe_link(self) -> '_2075.PlanetaryConnectorMultiNodeFELink':
        '''PlanetaryConnectorMultiNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.PlanetaryConnectorMultiNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetaryConnectorMultiNodeFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planet_based_fe_link(self) -> '_2076.PlanetBasedFELink':
        '''PlanetBasedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.PlanetBasedFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetBasedFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_planet_carrier_fe_link(self) -> '_2077.PlanetCarrierFELink':
        '''PlanetCarrierFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.PlanetCarrierFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PlanetCarrierFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_point_load_fe_link(self) -> '_2078.PointLoadFELink':
        '''PointLoadFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.PointLoadFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to PointLoadFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_fe_link(self) -> '_2079.RollingRingConnectionFELink':
        '''RollingRingConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.RollingRingConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to RollingRingConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_2080.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.ShaftHubConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_single_node_fe_link(self) -> '_2081.SingleNodeFELink':
        '''SingleNodeFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.SingleNodeFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
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
