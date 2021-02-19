'''_6266.py

SynchroniserSleeveLoadCase
'''


from mastapy.system_model.part_model.couplings import _2200
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6265
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserSleeveLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveLoadCase',)


class SynchroniserSleeveLoadCase(_6265.SynchroniserPartLoadCase):
    '''SynchroniserSleeveLoadCase

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2200.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
