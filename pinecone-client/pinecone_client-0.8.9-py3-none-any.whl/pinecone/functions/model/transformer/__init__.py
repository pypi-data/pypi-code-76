#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model import ModelFunction
from pinecone.protos import core_pb2
from pinecone.utils import load_numpy, dump_numpy

import numpy as np


class Transformer(ModelFunction):

    def setup(self):
        """
        Download and cache the model prior to serving
        :return:
        """

    def transform_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """
        Transforms given set of vectors given the raw data and metadta
        :param vectors: input vectors
        :param items: metdata for each vector
        :return: numpy vectors representing tranformed vectors
        """
        raise NotImplementedError

    def transform_numpy_vectors(self, msg_vectors: 'core_pb2.NdArray') -> 'core_pb2.NdArray':
        vectors = load_numpy(msg_vectors)
        transformed_vectors = self.transform_vectors(vectors)
        return dump_numpy(transformed_vectors)

    def handle_msg(self, msg: 'core_pb2.Request') -> 'core_pb2.Request':
        req_type = msg.WhichOneof('body')
        if req_type == 'index':
            msg.index.data.CopyFrom(self.transform_numpy_vectors(msg.index.data))
        elif req_type == 'query':
            msg.query.data.CopyFrom(self.transform_numpy_vectors(msg.query.data))
        return msg
