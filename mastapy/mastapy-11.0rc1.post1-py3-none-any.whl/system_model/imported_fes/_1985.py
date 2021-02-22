'''_1985.py

FEComponentWithBatchOptions
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1990
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_COMPONENT_WITH_BATCH_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'FEComponentWithBatchOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FEComponentWithBatchOptions',)


class FEComponentWithBatchOptions(_0.APIBase):
    '''FEComponentWithBatchOptions

    This is a mastapy class.
    '''

    TYPE = _FE_COMPONENT_WITH_BATCH_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEComponentWithBatchOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_component(self) -> 'str':
        '''str: 'FEComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEComponent

    @property
    def all_selected(self) -> 'bool':
        '''bool: 'AllSelected' is the original name of this property.'''

        return self.wrapped.AllSelected

    @all_selected.setter
    def all_selected(self, value: 'bool'):
        self.wrapped.AllSelected = bool(value) if value else False

    @property
    def fes(self) -> 'List[_1990.FEWithBatchOptions]':
        '''List[FEWithBatchOptions]: 'FEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEs, constructor.new(_1990.FEWithBatchOptions))
        return value

    @property
    def fes_with_external_files(self) -> 'List[_1990.FEWithBatchOptions]':
        '''List[FEWithBatchOptions]: 'FEsWithExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEsWithExternalFiles, constructor.new(_1990.FEWithBatchOptions))
        return value
