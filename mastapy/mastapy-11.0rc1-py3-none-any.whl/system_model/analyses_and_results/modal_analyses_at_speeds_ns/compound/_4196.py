'''_4196.py

CVTCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4165
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'CVTCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundModalAnalysesAtSpeeds',)


class CVTCompoundModalAnalysesAtSpeeds(_4165.BeltDriveCompoundModalAnalysesAtSpeeds):
    '''CVTCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
