'''_7176.py

PartCompoundAnalysis
'''


from mastapy.scripting import _7192
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7173
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'PartCompoundAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundAnalysis',)


class PartCompoundAnalysis(_7173.DesignEntityCompoundAnalysis):
    '''PartCompoundAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def two_d_drawing(self) -> '_7192.SMTBitmap':
        '''SMTBitmap: 'TwoDDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7192.SMTBitmap)(self.wrapped.TwoDDrawing) if self.wrapped.TwoDDrawing else None
