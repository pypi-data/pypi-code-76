'''_2457.py

CVTCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2426
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundSystemDeflection',)


class CVTCompoundSystemDeflection(_2426.BeltDriveCompoundSystemDeflection):
    '''CVTCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
