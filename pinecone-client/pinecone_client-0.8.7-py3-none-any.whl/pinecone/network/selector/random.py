#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.network.selector import SocketSelector
from pinecone.protos import core_pb2

from typing import List, Optional
import random


class RandomSelector(SocketSelector):

    @classmethod
    def select_socket(cls, orig_msg: 'core_pb2.Request', shards: int) -> List[Optional['core_pb2.Request']]:
        index = random.randint(0, shards - 1)
        return [orig_msg if i == index else None for i in range(0, shards)]
