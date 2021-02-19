'''_730.py

ConicalMeshManufacturingAnalysis
'''


from typing import List

from mastapy.gears.load_case.conical import _822
from mastapy._internal import constructor, conversion
from mastapy.gears.load_case.bevel import _827
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import _741, _725
from mastapy.gears.analysis import _1130
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MANUFACTURING_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshManufacturingAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshManufacturingAnalysis',)


class ConicalMeshManufacturingAnalysis(_1130.GearMeshImplementationAnalysis):
    '''ConicalMeshManufacturingAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MANUFACTURING_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshManufacturingAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_mesh_load_case(self) -> '_822.ConicalMeshLoadCase':
        '''ConicalMeshLoadCase: 'ConicalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _822.ConicalMeshLoadCase.TYPE not in self.wrapped.ConicalMeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast conical_mesh_load_case to ConicalMeshLoadCase. Expected: {}.'.format(self.wrapped.ConicalMeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalMeshLoadCase.__class__)(self.wrapped.ConicalMeshLoadCase) if self.wrapped.ConicalMeshLoadCase else None

    @property
    def tca(self) -> '_741.EaseOffBasedTCA':
        '''EaseOffBasedTCA: 'TCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_741.EaseOffBasedTCA)(self.wrapped.TCA) if self.wrapped.TCA else None

    @property
    def meshed_gears(self) -> 'List[_725.ConicalMeshedGearManufacturingAnalysis]':
        '''List[ConicalMeshedGearManufacturingAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_725.ConicalMeshedGearManufacturingAnalysis))
        return value
