#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import NamedTuple, Iterable
import numpy as np

from pinecone.utils import load_numpy, dump_numpy
from pinecone.protos import core_pb2

from pinecone.functions.model import ModelFunction


class QueryResult(NamedTuple):
    ids: Iterable[str] = None
    scores: Iterable[float] = None
    data: np.ndarray = None


class Postprocessor(ModelFunction):
    def transform(self, queries: np.ndarray, matches: Iterable[QueryResult]) -> Iterable[QueryResult]:
        """Transforms the scored matches.
        We only overwrite the original matches with fields in the transformed matches that are not None.
        """
        raise NotImplementedError

    def handle_msg(self, msg: "core_pb2.Request") -> "core_pb2.Request":
        req_type = msg.WhichOneof("body")
        if req_type == "query":
            queries = load_numpy(msg.query.data)
            matches = [
                QueryResult(
                    ids=match.ids, scores=match.scores, data=load_numpy(match.data) if msg.query.include_data else None
                )
                for match in msg.query.matches
            ]
            transformed_matches = self.transform(queries, matches)
            for match, match_tf in zip(msg.query.matches, transformed_matches):
                if match_tf.ids is not None:
                    match.ids[:] = match_tf.ids
                if match_tf.scores is not None:
                    match.scores[:] = match_tf.scores
                if match_tf.data is not None:
                    match.data.CopyFrom(dump_numpy(match_tf.data))
        return msg
