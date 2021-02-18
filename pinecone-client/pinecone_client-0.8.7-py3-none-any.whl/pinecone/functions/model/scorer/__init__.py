#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model import ModelFunction
from pinecone.protos import core_pb2
from pinecone.utils import load_numpy, clear_pb_repeated

import numpy as np

from typing import Iterable


class Scorer(ModelFunction):

    def score(self,
              data_queries: Iterable[np.ndarray],
              data_items: Iterable[Iterable[np.ndarray]]
              ) -> Iterable[Iterable[float]]:
        """
        Use a model to predictions scores. Each query is associated with an Iterable of items.
        The model makes a prediction for each query-item combination.
        :param data_queries:
        :param data_items: input array to model
        :return: numpy vector representing embedding
        """
        raise NotImplementedError

    def handle_msg(self, msg: 'core_pb2.Request') -> 'core_pb2.Request':
        """

        @type msg: object
        """
        query_vectors = load_numpy(msg.query.data)
        all_scores = self.score(query_vectors,(load_numpy(matches.data) for matches in msg.query.matches) )
        for query_vec, matches, scores in zip(query_vectors, msg.query.matches, all_scores):
            clear_pb_repeated(matches.scores)
            matches.scores.extend(scores)
        return msg
