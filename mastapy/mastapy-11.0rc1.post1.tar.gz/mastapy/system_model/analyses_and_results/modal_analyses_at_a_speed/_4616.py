'''_4616.py

ZerolBevelGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2224
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6617
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4506
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ZerolBevelGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysisAtASpeed',)


class ZerolBevelGearModalAnalysisAtASpeed(_4506.BevelGearModalAnalysisAtASpeed):
    '''ZerolBevelGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2224.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6617.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6617.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
