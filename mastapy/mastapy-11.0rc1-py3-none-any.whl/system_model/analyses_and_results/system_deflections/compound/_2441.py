'''_2441.py

ComponentCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2492
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ComponentCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundSystemDeflection',)


class ComponentCompoundSystemDeflection(_2492.PartCompoundSystemDeflection):
    '''ComponentCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
