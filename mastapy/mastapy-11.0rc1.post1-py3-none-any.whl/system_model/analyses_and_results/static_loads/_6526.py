'''_6526.py

GuideDxfModelLoadCase
'''


from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6468
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GuideDxfModelLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelLoadCase',)


class GuideDxfModelLoadCase(_6468.ComponentLoadCase):
    '''GuideDxfModelLoadCase

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
