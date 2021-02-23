#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.ranker import Ranker

import numpy as np


class DotProductRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_dotproduct(self, xx, uu):
        return np.einsum('ij,kj->ik', xx, uu)

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> Iterable[float]:
        return self.batch_dotproduct(vectors, q).flatten()
