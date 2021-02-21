#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Optional, Iterable, List

import numpy as np

from pinecone.functions.ranker import Ranker


class Aggregator(Ranker):

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> List[float]:
        return list(prev_scores)
