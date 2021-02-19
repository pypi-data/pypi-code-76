'''_5278.py

AbstractDesignStateLoadCaseGroup
'''


from mastapy._internal import constructor
from mastapy.scripting import _6555
from mastapy.system_model.analyses_and_results.load_case_groups import _5280
from mastapy._internal.python_net import python_net_import

_ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractDesignStateLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractDesignStateLoadCaseGroup',)


class AbstractDesignStateLoadCaseGroup(_5280.AbstractStaticLoadCaseGroup):
    '''AbstractDesignStateLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractDesignStateLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ratio(self) -> 'float':
        '''float: 'Ratio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Ratio

    @property
    def target_ratio(self) -> 'float':
        '''float: 'TargetRatio' is the original name of this property.'''

        return self.wrapped.TargetRatio

    @target_ratio.setter
    def target_ratio(self, value: 'float'):
        self.wrapped.TargetRatio = float(value) if value else 0.0

    @property
    def target_ratio_tolerance_absolute(self) -> 'float':
        '''float: 'TargetRatioToleranceAbsolute' is the original name of this property.'''

        return self.wrapped.TargetRatioToleranceAbsolute

    @target_ratio_tolerance_absolute.setter
    def target_ratio_tolerance_absolute(self, value: 'float'):
        self.wrapped.TargetRatioToleranceAbsolute = float(value) if value else 0.0

    @property
    def target_ratio_tolerance(self) -> 'float':
        '''float: 'TargetRatioTolerance' is the original name of this property.'''

        return self.wrapped.TargetRatioTolerance

    @target_ratio_tolerance.setter
    def target_ratio_tolerance(self, value: 'float'):
        self.wrapped.TargetRatioTolerance = float(value) if value else 0.0

    @property
    def twod_drawing_showing_power_flow(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'TwoDDrawingShowingPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.TwoDDrawingShowingPowerFlow) if self.wrapped.TwoDDrawingShowingPowerFlow else None
