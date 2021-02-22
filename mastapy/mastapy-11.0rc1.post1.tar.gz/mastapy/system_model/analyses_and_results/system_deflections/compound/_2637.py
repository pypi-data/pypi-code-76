'''_2637.py

VirtualComponentCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2591
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'VirtualComponentCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundSystemDeflection',)


class VirtualComponentCompoundSystemDeflection(_2591.MountableComponentCompoundSystemDeflection):
    '''VirtualComponentCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
