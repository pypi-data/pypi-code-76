'''_2630.py

SynchroniserPartCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2552
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SynchroniserPartCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPartCompoundSystemDeflection',)


class SynchroniserPartCompoundSystemDeflection(_2552.CouplingHalfCompoundSystemDeflection):
    '''SynchroniserPartCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserPartCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
