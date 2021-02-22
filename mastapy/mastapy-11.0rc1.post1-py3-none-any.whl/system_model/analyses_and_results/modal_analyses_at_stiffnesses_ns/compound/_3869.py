'''_3869.py

AbstractAssemblyCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3942
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'AbstractAssemblyCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundModalAnalysesAtStiffnesses',)


class AbstractAssemblyCompoundModalAnalysesAtStiffnesses(_3942.PartCompoundModalAnalysesAtStiffnesses):
    '''AbstractAssemblyCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
