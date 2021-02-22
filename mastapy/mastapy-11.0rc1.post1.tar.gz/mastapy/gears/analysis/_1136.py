'''_1136.py

GearSetImplementationAnalysisAbstract
'''


from mastapy.gears.analysis import _1133
from mastapy._internal.python_net import python_net_import

_GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearSetImplementationAnalysisAbstract')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetImplementationAnalysisAbstract',)


class GearSetImplementationAnalysisAbstract(_1133.GearSetDesignAnalysis):
    '''GearSetImplementationAnalysisAbstract

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetImplementationAnalysisAbstract.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
