"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""
from web3.types import BlockData

from brownie.network.state import Chain as _Chain
from brownie import web3


class Chain(_Chain):

    def __init__(self):
        super().__init__()

    def get_block(self, block_number: int) -> BlockData:
        """
        Return information about a block by block number.

        Arguments
        ---------
        block_number : int
            Integer of a block number. If the value is negative, the block returned
            is relative to the most recently mined block, e.g. `chain[-1]` returns
            the most recent block.

        Returns
        -------
        BlockData
            web3 block data object
        """
        if not isinstance(block_number, int):
            raise TypeError("Block height must be given as an integer")
        if block_number < 0:
            block_number = web3.eth.blockNumber + 1 + block_number
        block = web3.eth.getBlock(block_number, full_transactions=True)
        if block["timestamp"] > self._block_gas_time:
            self._block_gas_limit = block["gasLimit"]
            self._block_gas_time = block["timestamp"]
        return block
