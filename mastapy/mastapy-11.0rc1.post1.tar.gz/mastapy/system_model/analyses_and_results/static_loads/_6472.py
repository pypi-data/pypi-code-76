'''_6472.py

ConceptGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6520
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearLoadCase',)


class ConceptGearLoadCase(_6520.GearLoadCase):
    '''ConceptGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
