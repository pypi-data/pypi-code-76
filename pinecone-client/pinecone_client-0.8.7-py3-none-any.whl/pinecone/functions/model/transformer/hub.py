#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model.transformer import Transformer
from pinecone.functions.model.hub import HubModel
from pinecone.utils import dump_numpy, load_numpy
from pinecone.protos import core_pb2

import numpy as np


class HubTransformer (HubModel, Transformer):

    async def transform_vectors(self, vectors: np.ndarray, timeout: float = 30) -> np.ndarray:
        query = core_pb2.QueryRequest(data=dump_numpy(vectors))
        response = await self.call_remote(core_pb2.Request(query=query, path='read'), timeout=timeout)
        return load_numpy(response.query.data)
