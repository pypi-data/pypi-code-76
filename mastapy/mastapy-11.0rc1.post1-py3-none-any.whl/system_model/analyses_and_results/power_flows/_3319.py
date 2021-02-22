'''_3319.py

CVTPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2180
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3288
from mastapy._internal.python_net import python_net_import

_CVT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CVTPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPowerFlow',)


class CVTPowerFlow(_3288.BeltDrivePowerFlow):
    '''CVTPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CVT_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2180.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
