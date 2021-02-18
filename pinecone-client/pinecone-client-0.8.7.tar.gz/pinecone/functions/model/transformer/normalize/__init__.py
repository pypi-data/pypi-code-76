#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model.transformer import Transformer

import numpy as np


class NormalizeTransformer(Transformer):
    """
    Normalize vectors (l2-norm)
    """
    def transform_vectors(self, vectors: np.ndarray) -> np.ndarray:
        data_array = np.array(vectors)
        data_norm = np.sqrt(np.einsum('ij,ij->i',data_array, data_array))
        col_dim = data_array.shape[1]
        return data_array / np.broadcast_to(data_norm, (col_dim,) + data_norm.shape).T
