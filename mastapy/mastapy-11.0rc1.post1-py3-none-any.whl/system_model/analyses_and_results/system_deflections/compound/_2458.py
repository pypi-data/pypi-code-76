'''_2458.py

CVTPulleyCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2501
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTPulleyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundSystemDeflection',)


class CVTPulleyCompoundSystemDeflection(_2501.PulleyCompoundSystemDeflection):
    '''CVTPulleyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
