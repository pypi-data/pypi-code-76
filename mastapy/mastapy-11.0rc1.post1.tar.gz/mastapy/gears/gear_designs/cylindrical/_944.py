'''_944.py

CylindricalGearDesignConstraintsDatabase
'''


from mastapy.utility.databases import _1554
from mastapy.gears.gear_designs.cylindrical import _943
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraintsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraintsDatabase',)


class CylindricalGearDesignConstraintsDatabase(_1554.NamedDatabase['_943.CylindricalGearDesignConstraints']):
    '''CylindricalGearDesignConstraintsDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraintsDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
