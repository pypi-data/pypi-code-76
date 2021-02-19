#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.ranker import Ranker

import numpy as np


class EuclideanRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_euclidean(self, xx, uu):
        xx_normed_squared = np.einsum('ij,ij->i', xx, xx)
        uu_normed_squared = np.einsum('ij,ij->i', uu, uu)
        dot_product = np.einsum('ij,kj->ik', xx, uu)
        return -xx_normed_squared[:, np.newaxis] - uu_normed_squared + 2 * dot_product
    

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> Iterable[float]:
        return self.batch_euclidean(vectors, q).flatten()
