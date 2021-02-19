'''_201.py

RealCMSResults
'''


from mastapy.nodal_analysis.states import _115, _114
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis.component_mode_synthesis import _198
from mastapy._internal.python_net import python_net_import

_REAL_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'RealCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RealCMSResults',)


class RealCMSResults(_198.CMSResults):
    '''RealCMSResults

    This is a mastapy class.
    '''

    TYPE = _REAL_CMS_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RealCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_displacements(self) -> '_115.NodeVectorState':
        '''NodeVectorState: 'NodeDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _115.NodeVectorState.TYPE not in self.wrapped.NodeDisplacements.__class__.__mro__:
            raise CastException('Failed to cast node_displacements to NodeVectorState. Expected: {}.'.format(self.wrapped.NodeDisplacements.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NodeDisplacements.__class__)(self.wrapped.NodeDisplacements) if self.wrapped.NodeDisplacements else None
