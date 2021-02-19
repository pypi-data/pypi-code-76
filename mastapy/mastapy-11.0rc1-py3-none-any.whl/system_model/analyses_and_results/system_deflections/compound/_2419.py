'''_2419.py

AbstractShaftOrHousingCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2441
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AbstractShaftOrHousingCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingCompoundSystemDeflection',)


class AbstractShaftOrHousingCompoundSystemDeflection(_2441.ComponentCompoundSystemDeflection):
    '''AbstractShaftOrHousingCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
