#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import numpy as np

from pinecone.utils import load_numpy, dump_numpy
from pinecone.protos import core_pb2

from pinecone.functions.model import ModelFunction


class Preprocessor(ModelFunction):
    def transform(self, vectors: np.ndarray) -> np.ndarray:
        """Transforms vectors."""
        raise NotImplementedError

    def handle_msg(self, msg: "core_pb2.Request") -> "core_pb2.Request":
        req_type = msg.WhichOneof("body")
        if req_type == "index":
            vectors = load_numpy(msg.index.data)
            msg.index.data.CopyFrom(dump_numpy(self.transform(vectors)))
        elif req_type == "query":
            vectors = load_numpy(msg.query.data)
            msg.query.data.CopyFrom(dump_numpy(self.transform(vectors)))
        return msg