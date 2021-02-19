'''_875.py

DesignConstraintsCollection
'''


from typing import List

from mastapy.utility.property import _1561
from mastapy.gears.gear_designs import _873
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1555
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINTS_COLLECTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintsCollection')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintsCollection',)


class DesignConstraintsCollection(_1555.NamedDatabaseItem):
    '''DesignConstraintsCollection

    This is a mastapy class.
    '''

    TYPE = _DESIGN_CONSTRAINTS_COLLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignConstraintsCollection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints(self) -> 'List[_1561.DeletableCollectionMember[_873.DesignConstraint]]':
        '''List[DeletableCollectionMember[DesignConstraint]]: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignConstraints, constructor.new(_1561.DeletableCollectionMember)[_873.DesignConstraint])
        return value
