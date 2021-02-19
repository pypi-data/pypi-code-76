'''_5765.py

ConicalGearCompoundGearWhineAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5786
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ConicalGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundGearWhineAnalysis',)


class ConicalGearCompoundGearWhineAnalysis(_5786.GearCompoundGearWhineAnalysis):
    '''ConicalGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearCompoundGearWhineAnalysis]':
        '''List[ConicalGearCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearCompoundGearWhineAnalysis))
        return value
