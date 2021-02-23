#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable
import numpy as np

from pinecone.utils import load_numpy
from pinecone.grpc import GRPCClient

from pinecone.functions.model import HubFunction
from . import QueryResult


class HubPostprocessor(HubFunction):
    """Useful for local testing. Mimics a query request sent to a HubFunction hosting a Postprocessor image."""

    async def transform(self, queries: np.ndarray, matches: Iterable[QueryResult], timeout: float = 30) -> Iterable[QueryResult]:
        grpc = GRPCClient()
        msg = grpc.get_query_request(data=queries, matches=[mat._asdict() for mat in matches], path="read")
        response = await self.handle_msg(msg, timeout)

        result = []
        for match in response.query.matches:
            result.append(
                QueryResult(ids=match.ids, scores=match.scores, data=load_numpy(match.data) if match.data else None)
            )
        return result
