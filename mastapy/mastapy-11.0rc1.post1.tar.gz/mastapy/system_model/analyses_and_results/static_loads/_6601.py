'''_6601.py

SynchroniserSleeveLoadCase
'''


from mastapy.system_model.part_model.couplings import _2277
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6600
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserSleeveLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveLoadCase',)


class SynchroniserSleeveLoadCase(_6600.SynchroniserPartLoadCase):
    '''SynchroniserSleeveLoadCase

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2277.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
