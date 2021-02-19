'''_3329.py

FaceGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2126
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6183
from mastapy.gears.rating.face import _247
from mastapy.system_model.analyses_and_results.power_flows import _3333
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FaceGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearPowerFlow',)


class FaceGearPowerFlow(_3333.GearPowerFlow):
    '''FaceGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6183.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6183.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_247.FaceGearRating':
        '''FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_247.FaceGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
