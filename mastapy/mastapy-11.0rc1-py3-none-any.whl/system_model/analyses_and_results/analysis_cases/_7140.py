'''_7140.py

DesignEntityCompoundAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results import _2297, _2295
from mastapy._internal.python_net import python_net_import

_DESIGN_ENTITY_COMPOUND_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'DesignEntityCompoundAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignEntityCompoundAnalysis',)


class DesignEntityCompoundAnalysis(_2295.DesignEntityAnalysis):
    '''DesignEntityCompoundAnalysis

    This is a mastapy class.
    '''

    TYPE = _DESIGN_ENTITY_COMPOUND_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignEntityCompoundAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def real_name_in_context_name(self) -> 'str':
        '''str: 'RealNameInContextName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RealNameInContextName

    @property
    def analysis_time(self) -> 'float':
        '''float: 'AnalysisTime' is the original name of this property.'''

        return self.wrapped.AnalysisTime

    @analysis_time.setter
    def analysis_time(self, value: 'float'):
        self.wrapped.AnalysisTime = float(value) if value else 0.0

    @property
    def load_case_analyses_ready(self) -> 'List[_2297.DesignEntitySingleContextAnalysis]':
        '''List[DesignEntitySingleContextAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2297.DesignEntitySingleContextAnalysis))
        return value
