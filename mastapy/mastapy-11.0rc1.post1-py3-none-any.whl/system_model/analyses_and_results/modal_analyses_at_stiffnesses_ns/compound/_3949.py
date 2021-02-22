'''_3949.py

CVTCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3918
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'CVTCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundModalAnalysesAtStiffnesses',)


class CVTCompoundModalAnalysesAtStiffnesses(_3918.BeltDriveCompoundModalAnalysesAtStiffnesses):
    '''CVTCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
