'''_4192.py

CouplingCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4247
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'CouplingCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundModalAnalysesAtSpeeds',)


class CouplingCompoundModalAnalysesAtSpeeds(_4247.SpecialisedAssemblyCompoundModalAnalysesAtSpeeds):
    '''CouplingCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
