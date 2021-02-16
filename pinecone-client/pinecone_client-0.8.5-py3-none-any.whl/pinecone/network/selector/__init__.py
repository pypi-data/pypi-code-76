#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.protos import core_pb2
from typing import List, Optional

import abc


class SocketSelector(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def select_socket(cls, orig_msg: 'core_pb2.Request', shards: int) -> List[Optional['core_pb2.Request']]:
        raise NotImplementedError
