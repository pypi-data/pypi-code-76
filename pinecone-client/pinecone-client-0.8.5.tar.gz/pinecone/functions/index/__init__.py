#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions import Function

from abc import abstractmethod
from typing import Dict, Union


class Index (Function):

    """
    Generic interface for defining an index
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @abstractmethod
    def size(self) -> int:
        """
        Size of the index
        :return: the number of items in the index
        """
        raise NotImplementedError

    def get_stats(self) -> Dict[str, Union[int, float, str]]:
        return {'size': self.size()}

    

