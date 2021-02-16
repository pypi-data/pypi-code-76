#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.ranker import Ranker

import numpy as np


class CosineRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_norm(self, x):
        xx_row_norms = np.sqrt(np.einsum('ij,ij->i', x, x))
        xx_row_norms[xx_row_norms == 0] = 1  # don't normalize zero vectors
        return x / xx_row_norms[:, np.newaxis]

    def norm(self, q):
        return q / np.sqrt(np.einsum('ij,ij->i', q, q))

    def sim_cosine(self, x, u):
        norm_x = np.sqrt(np.einsum('i,i->', x, x))
        norm_u = np.sqrt(np.einsum('i,i->', u, u))
        ret = np.einsum('i,i->', x, u) / (norm_x * norm_u)
        return ret

    def batch_cosine(self, x, q):
        x_normed = self.batch_norm(x)
        q_normed = self.norm(q)
        return np.einsum('ij,kj->ik', x_normed, q_normed)

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> Iterable[float]:
        return self.batch_cosine(vectors, q).flatten()
