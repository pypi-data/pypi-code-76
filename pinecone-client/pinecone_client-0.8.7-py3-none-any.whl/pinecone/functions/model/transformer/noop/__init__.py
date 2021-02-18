#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.model.transformer import Transformer
from pinecone import utils


@utils.hubify
class NoOpTransformer(Transformer):
    def transform_vectors(self, vectors):
        return vectors
