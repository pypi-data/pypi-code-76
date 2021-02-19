#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.index import Index
from pinecone.protos import core_pb2
from pinecone.utils import load_numpy, dump_numpy
from pinecone.utils.constants import MAX_ID_LENGTH
import numpy as np

from typing import Iterable, Tuple
from abc import abstractmethod


class VectorIndex(Index):
    """
    Generic interface for defining vector index
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def add_data(self, data: np.ndarray, ids: Iterable[str]):
        """
        Add data to an index
        :param data:
        :param vectors: list of vectors to add
        :param ids: list of ids that correspond to those vectors
        """
        raise NotImplementedError

    @abstractmethod
    def delete_data(self, ids: Iterable[str]):
        """
        Delete data points from index by id
        :param ids: ids to delete
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def query(self, vectors: np.ndarray, k: int, include_data: bool = False) -> (Iterable[Tuple[Iterable[str],
                                                                                 Iterable[float], np.ndarray]]):
        """
        Query an index
        :param include_data: If True, returns data associated with the matched ids.
        :param vectors: Vectors to query
        :param k: number of similar items to return
        :return: list of ids of similar items for each vector
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_data(self, ids: Iterable[str], default: np.ndarray = None) -> Iterable[np.ndarray]:
        """
        Fetch raw vectors from the index
        :param ids: ids to fetch
        :param default: default value for cases where the vector the id wasn't found
        :return: list of vectors associated with the received ids
        """
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        """
        :return: number of items in the index
        """

    @abstractmethod
    def dimension(self) -> int:
        """
        :return: dimension of the indexed vectors
        """

    @staticmethod
    def downcast_data(data: np.ndarray) -> np.ndarray:
        if not data.dtype == np.float32:
            return data.astype('float32', casting='same_kind')
        return data

    def validate_dimension(self, data: np.ndarray):
        if self.dimension() and data.shape[1] != self.dimension():
            raise ValueError(f"Data dimension must be consistent {data.shape[1]} != {self.dimension()}")

    @staticmethod
    def validate_ids(ids: Iterable[str]):
        if MAX_ID_LENGTH == 0:
            return  # no limit
        if any(len(id_) > MAX_ID_LENGTH for id_ in ids):
            raise ValueError(f"Vector IDs should be no longer than {MAX_ID_LENGTH} characters")

    def handle_msg(self, msg: 'core_pb2.Request') -> 'core_pb2.Request':
        req_type = msg.WhichOneof('body')
        if req_type == 'delete':
            self.delete_data(msg.delete.ids)
        elif req_type == 'index':
            if self.full:
                raise RuntimeError("Index is full, cannot accept upserts")
            VectorIndex.validate_ids(msg.index.ids)
            data = VectorIndex.downcast_data(load_numpy(msg.index.data))
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            self.validate_dimension(data)
            self.add_data(data, msg.index.ids)
            msg.index.data.Clear()  # data is not needed along the way
        elif req_type == 'query':
            vectors = VectorIndex.downcast_data(load_numpy(msg.query.data))
            if len(vectors.shape) == 1:
                vectors = vectors.reshape(1, -1)
            self.validate_dimension(vectors)
            all_matches = self.query(vectors, msg.query.top_k, msg.query.include_data)
            for matches in all_matches:
                ids, scores, data = matches
                if msg.query.include_data:
                    msg.query.matches.append(core_pb2.ScoredResults(ids=ids, scores=scores, data=dump_numpy(data)))
                else:
                    msg.query.matches.append(core_pb2.ScoredResults(ids=ids, scores=scores))
        elif req_type == 'info':
            msg.info.index_size += self.size()
        elif req_type == 'fetch':
            default_value = np.array([], dtype=np.float32)
            msg.fetch.vectors.extend(
                [dump_numpy(vector) for vector in self.fetch_data(msg.fetch.ids, default=default_value)])
        return msg
