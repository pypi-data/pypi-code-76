#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.network.selector import SocketSelector
from pinecone.protos import core_pb2

from typing import List, Optional


class AllSelector(SocketSelector):

    @classmethod
    def select_socket(cls, orig_msg: 'core_pb2.Request', shards: int) -> List[Optional['core_pb2.Request']]:
        return [orig_msg] * shards
