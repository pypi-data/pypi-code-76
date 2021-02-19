'''_6551.py

MeasurementComponentLoadCase
'''


from mastapy.system_model.part_model import _2136
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6613
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MeasurementComponentLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentLoadCase',)


class MeasurementComponentLoadCase(_6613.VirtualComponentLoadCase):
    '''MeasurementComponentLoadCase

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2136.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
