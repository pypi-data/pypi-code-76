'''_1990.py

FEWithBatchOptions
'''


from mastapy._internal import constructor
from mastapy.system_model.imported_fes import _1992
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_WITH_BATCH_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'FEWithBatchOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FEWithBatchOptions',)


class FEWithBatchOptions(_0.APIBase):
    '''FEWithBatchOptions

    This is a mastapy class.
    '''

    TYPE = _FE_WITH_BATCH_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEWithBatchOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def run_condensation(self) -> 'bool':
        '''bool: 'RunCondensation' is the original name of this property.'''

        return self.wrapped.RunCondensation

    @run_condensation.setter
    def run_condensation(self, value: 'bool'):
        self.wrapped.RunCondensation = bool(value) if value else False

    @property
    def fe_model(self) -> 'str':
        '''str: 'FEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEModel

    @property
    def load_mesh(self) -> 'bool':
        '''bool: 'LoadMesh' is the original name of this property.'''

        return self.wrapped.LoadMesh

    @load_mesh.setter
    def load_mesh(self, value: 'bool'):
        self.wrapped.LoadMesh = bool(value) if value else False

    @property
    def unload_mesh(self) -> 'bool':
        '''bool: 'UnloadMesh' is the original name of this property.'''

        return self.wrapped.UnloadMesh

    @unload_mesh.setter
    def unload_mesh(self, value: 'bool'):
        self.wrapped.UnloadMesh = bool(value) if value else False

    @property
    def load_vectors(self) -> 'bool':
        '''bool: 'LoadVectors' is the original name of this property.'''

        return self.wrapped.LoadVectors

    @load_vectors.setter
    def load_vectors(self, value: 'bool'):
        self.wrapped.LoadVectors = bool(value) if value else False

    @property
    def load_mesh_and_vectors(self) -> 'bool':
        '''bool: 'LoadMeshAndVectors' is the original name of this property.'''

        return self.wrapped.LoadMeshAndVectors

    @load_mesh_and_vectors.setter
    def load_mesh_and_vectors(self, value: 'bool'):
        self.wrapped.LoadMeshAndVectors = bool(value) if value else False

    @property
    def unload_vectors(self) -> 'bool':
        '''bool: 'UnloadVectors' is the original name of this property.'''

        return self.wrapped.UnloadVectors

    @unload_vectors.setter
    def unload_vectors(self, value: 'bool'):
        self.wrapped.UnloadVectors = bool(value) if value else False

    @property
    def fe(self) -> '_1992.ImportedFE':
        '''ImportedFE: 'FE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.ImportedFE)(self.wrapped.FE) if self.wrapped.FE else None
