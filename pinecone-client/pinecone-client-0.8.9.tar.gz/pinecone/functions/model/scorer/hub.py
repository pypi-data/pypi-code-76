#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model.scorer import Scorer
from pinecone.functions.model.hub import HubModel
from pinecone.utils import dump_numpy
from pinecone.protos import core_pb2

import numpy as np

from typing import Iterable


class HubScorer(HubModel, Scorer):

    async def score(self,
                    data_queries: Iterable[np.ndarray],
                    data_items: Iterable[Iterable[np.ndarray]]
                    ) -> Iterable[Iterable[float]]:

        request = self.build_request(data_queries, data_items)
        response = await self.call_remote(request)
        return [matches.scores for matches in response.query.matches]

    @staticmethod
    def build_request(data_queries, data_items):
        matches = [core_pb2.ScoredResults(
            data=dump_numpy(np.array(items))) for items in data_items]
        request = core_pb2.QueryRequest(data=dump_numpy(np.array(data_queries)), matches=matches)
        return core_pb2.Request(query=request, path='read')
