'''_4071.py

CVTModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2180
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4039
from mastapy._internal.python_net import python_net_import

_CVT_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CVTModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTModalAnalysesAtSpeeds',)


class CVTModalAnalysesAtSpeeds(_4039.BeltDriveModalAnalysesAtSpeeds):
    '''CVTModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CVT_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2180.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
