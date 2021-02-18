#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.network.selector import SocketSelector

from pinecone.utils import load_numpy, dump_numpy
from pinecone.protos import core_pb2
from typing import List, Optional
import hashlib


def hash_id(item_id: str) -> int:
    return int(hashlib.md5(item_id.encode('utf-8')).hexdigest(), 16)


class ShardSelector(SocketSelector):

    @classmethod
    def shard_msg(cls, msg: 'core_pb2.Request', req_type: str, shards: int) -> List[Optional['core_pb2.Request']]:
        req = getattr(msg, req_type)
        hashed_ids = [hash_id(id_) for id_ in req.ids]
        shard_msgs = [core_pb2.Request() for i in range(shards)]
        data = load_numpy(req.data) if req_type == 'index' else None
        for shard_id, new_msg in enumerate(shard_msgs):
            new_msg.CopyFrom(msg)
            relevant_indices = [i for i in range(len(hashed_ids)) if (
                    hashed_ids[i] % shards) == shard_id]
            new_req = getattr(new_msg, req_type)
            relevant_ids = [new_req.ids[i] for i in relevant_indices]
            del new_req.ids[:]
            new_req.ids.extend(relevant_ids)
            if data is not None and len(data) > 0:
                new_req.data.CopyFrom(dump_numpy(data[relevant_indices, :]))
        return shard_msgs

    @classmethod
    def select_socket(cls, msg: 'core_pb2.Request', shards: int) -> List[Optional['core_pb2.Request']]:
        req_type = msg.WhichOneof('body')
        if req_type in ['info', 'query'] or shards <= 1:
            return [msg] * shards
        return ShardSelector.shard_msg(msg, req_type, shards)
