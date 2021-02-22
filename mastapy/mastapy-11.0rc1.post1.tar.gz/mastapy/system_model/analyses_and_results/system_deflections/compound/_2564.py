'''_2564.py

DatumCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2413
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2538
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'DatumCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundSystemDeflection',)


class DatumCompoundSystemDeflection(_2538.ComponentCompoundSystemDeflection):
    '''DatumCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2122.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2413.DatumSystemDeflection]':
        '''List[DatumSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2413.DatumSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2413.DatumSystemDeflection]':
        '''List[DatumSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2413.DatumSystemDeflection))
        return value
