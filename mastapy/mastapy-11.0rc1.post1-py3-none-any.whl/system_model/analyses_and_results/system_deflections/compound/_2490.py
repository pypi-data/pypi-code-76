'''_2490.py

MountableComponentCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2441
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'MountableComponentCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundSystemDeflection',)


class MountableComponentCompoundSystemDeflection(_2441.ComponentCompoundSystemDeflection):
    '''MountableComponentCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
