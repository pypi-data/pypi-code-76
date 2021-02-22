'''_2215.py

CycloidalDisc
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.cycloidal import _1217, _1218, _1224
from mastapy.system_model.part_model import _2109, _2085
from mastapy.materials import _234, _212
from mastapy.shafts import _24
from mastapy._internal.cast_exception import CastException
from mastapy.gears.materials import (
    _529, _531, _533, _537,
    _540, _543, _547, _549
)
from mastapy.detailed_rigid_connectors.splines import _1179
from mastapy.bolts import _1227, _1231
from mastapy.system_model.connections_and_sockets.cycloidal import _1991

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDisc',)


class CycloidalDisc(_2085.AbstractShaft):
    '''CycloidalDisc

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDisc.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hole_diameter_for_eccentric_bearing(self) -> 'float':
        '''float: 'HoleDiameterForEccentricBearing' is the original name of this property.'''

        return self.wrapped.HoleDiameterForEccentricBearing

    @hole_diameter_for_eccentric_bearing.setter
    def hole_diameter_for_eccentric_bearing(self, value: 'float'):
        self.wrapped.HoleDiameterForEccentricBearing = float(value) if value else 0.0

    @property
    def bore_diameter(self) -> 'float':
        '''float: 'BoreDiameter' is the original name of this property.'''

        return self.wrapped.BoreDiameter

    @bore_diameter.setter
    def bore_diameter(self, value: 'float'):
        self.wrapped.BoreDiameter = float(value) if value else 0.0

    @property
    def number_of_planetary_sockets(self) -> 'int':
        '''int: 'NumberOfPlanetarySockets' is the original name of this property.'''

        return self.wrapped.NumberOfPlanetarySockets

    @number_of_planetary_sockets.setter
    def number_of_planetary_sockets(self, value: 'int'):
        self.wrapped.NumberOfPlanetarySockets = int(value) if value else 0

    @property
    def disc_material_database(self) -> 'str':
        '''str: 'DiscMaterialDatabase' is the original name of this property.'''

        return self.wrapped.DiscMaterialDatabase.SelectedItemName

    @disc_material_database.setter
    def disc_material_database(self, value: 'str'):
        self.wrapped.DiscMaterialDatabase.SetSelectedItem(str(value) if value else None)

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def cycloidal_disc_design(self) -> '_1217.CycloidalDiscDesign':
        '''CycloidalDiscDesign: 'CycloidalDiscDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1217.CycloidalDiscDesign)(self.wrapped.CycloidalDiscDesign) if self.wrapped.CycloidalDiscDesign else None

    @property
    def load_sharing_settings(self) -> '_2109.LoadSharingSettings':
        '''LoadSharingSettings: 'LoadSharingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2109.LoadSharingSettings)(self.wrapped.LoadSharingSettings) if self.wrapped.LoadSharingSettings else None

    @property
    def disc_material(self) -> '_234.Material':
        '''Material: 'DiscMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _234.Material.TYPE not in self.wrapped.DiscMaterial.__class__.__mro__:
            raise CastException('Failed to cast disc_material to Material. Expected: {}.'.format(self.wrapped.DiscMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DiscMaterial.__class__)(self.wrapped.DiscMaterial) if self.wrapped.DiscMaterial else None

    @property
    def planetary_bearing_sockets(self) -> 'List[_1991.CycloidalDiscPlanetaryBearingSocket]':
        '''List[CycloidalDiscPlanetaryBearingSocket]: 'PlanetaryBearingSockets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetaryBearingSockets, constructor.new(_1991.CycloidalDiscPlanetaryBearingSocket))
        return value
