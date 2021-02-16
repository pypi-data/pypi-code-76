#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import numpy as np

from pinecone.utils import load_numpy
from pinecone.grpc import GRPCClient

from pinecone.functions.model import HubFunction


class HubPreprocessor(HubFunction):
    """Useful for local testing. Mimics a query request sent to a HubFunction hosting a Preprocessor image."""

    async def transform(self, vectors: np.ndarray, timeout: float = 30) -> np.ndarray:
        grpc = GRPCClient()
        msg = grpc.get_query_request(data=vectors, path="read")
        response = await self.handle_msg(msg, timeout)
        return load_numpy(response.query.data)
