#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.model.scorer import Scorer
from pinecone import utils

import numpy as np


@utils.hubify
class DotScorer(Scorer):

    def score(self,
              data_queries: Iterable[np.ndarray],
              data_items: Iterable[Iterable[np.ndarray]]
              ) -> Iterable[Iterable[float]]:
        return [list(np.dot(queries, np.transpose(items)).tolist()) for queries, items in zip(data_queries, data_items)]
