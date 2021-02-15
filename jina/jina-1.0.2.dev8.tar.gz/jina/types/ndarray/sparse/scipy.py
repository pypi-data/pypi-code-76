from typing import List

import numpy as np

from . import BaseSparseNdArray
from ....proto import jina_pb2

if False:
    import scipy.sparse

__all__ = ['SparseNdArray']


class SparseNdArray(BaseSparseNdArray):
    """
    Scipy powered sparse ndarray.

    .. warning::
        scipy only supports ndim=2

    .. seealso::
        https://docs.scipy.org/doc/scipy/reference/sparse.html

    :param proto: the protobuf message, when not given then create a new one via :meth:`get_null_proto`
    :param sp_format: the sparse format of the scipy matrix. one of 'coo', 'bsr', 'csc', 'csr'.
    """

    def __init__(self, proto: 'jina_pb2.SparseNdArrayProto' = None, sp_format: str = 'coo', *args, **kwargs):
        """Set constructor method."""
        import scipy.sparse
        super().__init__(proto, *args, **kwargs)
        support_fmt = {'coo', 'bsr', 'csc', 'csr'}
        if sp_format in support_fmt:
            self.spmat_fn = getattr(scipy.sparse, f'{sp_format}_matrix')
        else:
            raise ValueError(f'{sp_format} sparse matrix is not supported, please choose one of those: {support_fmt}')

    def sparse_constructor(self, indices: 'np.ndarray', values: 'np.ndarray',
                           shape: List[int]) -> 'scipy.sparse.spmatrix':
        """
        Sparse NdArray constructor for scipy.sparse.spmatrix.

        :param indices: the indices of the sparse array
        :param values: the values of the sparse array
        :param shape: the shape of the sparse array
        :return: SparseTensor
        """
        if indices.shape[-1] != 2:
            raise ValueError(f'scipy backend only supports ndim=2 sparse matrix, given {indices.shape}')
        return self.spmat_fn((values, indices.T), shape=shape)

    def sparse_parser(self, value: 'scipy.sparse.spmatrix'):
        """
        Parse a scipy.sparse.spmatrix to indices, values and shape.

        :param value: the scipy.sparse.spmatrix.
        :return: a Dict with three entries {'indices': ..., 'values':..., 'shape':...}
        """
        v = value.tocoo()
        return {'indices': np.stack([v.row, v.col], axis=1),
                'values': v.data,
                'shape': v.shape}
