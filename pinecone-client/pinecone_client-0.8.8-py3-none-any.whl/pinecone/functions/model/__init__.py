#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions import Function
from pinecone.protos import core_pb2
from .hub import HubModel


class ModelFunction(Function):
    def setup(self):
        """
        Download and cache the model prior to serving
        :return:
        """


class HubFunction(HubModel, ModelFunction):
    def __init__(self, image: str, config: dict = None, **kwargs):
        """A special Pinecone Function that loads models from the Model Hub.

        :param image: a Pinecone Model Hub docker image URI
        :type image: str
        :param config: configurations for the model, defaults to None
        :type config: dict, optional
        """
        super().__init__(image=image, config=config, **kwargs)

    async def handle_msg(self, msg: "core_pb2.Request", timeout: float = 30) -> "core_pb2.Request":
        return await self.call_remote(msg, timeout)
