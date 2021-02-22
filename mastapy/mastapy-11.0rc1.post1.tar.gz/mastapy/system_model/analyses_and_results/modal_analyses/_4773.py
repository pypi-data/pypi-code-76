'''_4773.py

ConceptCouplingConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2020
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6469
from mastapy.system_model.analyses_and_results.system_deflections import _2381
from mastapy.system_model.analyses_and_results.modal_analyses import _4785
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ConceptCouplingConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionModalAnalysis',)


class ConceptCouplingConnectionModalAnalysis(_4785.CouplingConnectionModalAnalysis):
    '''ConceptCouplingConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2020.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6469.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6469.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2381.ConceptCouplingConnectionSystemDeflection':
        '''ConceptCouplingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2381.ConceptCouplingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
