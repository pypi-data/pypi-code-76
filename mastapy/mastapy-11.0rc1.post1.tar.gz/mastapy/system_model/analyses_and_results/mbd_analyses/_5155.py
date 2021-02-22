'''_5155.py

StraightBevelSunGearMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5149
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelSunGearMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearMultibodyDynamicsAnalysis',)


class StraightBevelSunGearMultibodyDynamicsAnalysis(_5149.StraightBevelDiffGearMultibodyDynamicsAnalysis):
    '''StraightBevelSunGearMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2221.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
