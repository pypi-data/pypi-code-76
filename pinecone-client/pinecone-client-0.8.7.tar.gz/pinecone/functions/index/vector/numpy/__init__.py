#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable, Tuple

import numpy as np

from pinecone.functions.index.vector import VectorIndex


class NumpyIndex(VectorIndex):

    def setup(self):
        self._ids = []
        self._vectors = None

    def add_data(self, data: np.ndarray, ids: Iterable[str]):
        self._ids.extend(ids)
        if self._vectors:
            self._vectors = np.concatenate((self._vectors, data))
        else:
            self._vectors = data

    def size(self) -> int:
        return len(self._ids)

    def query(self, vectors: np.ndarray, k: int) -> (Iterable[Tuple[Iterable[str], Iterable[float]]]):
        results = []
        for vector in vectors:
            scores = np.dot(vector, self._vectors).flatten()
            idx = scores.argsort()
            results.append(([self._ids[i] for i in idx][:k], [scores[i] for i in idx][:k]))
        return results
