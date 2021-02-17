"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os

from web3.types import BlockIdentifier
from moneyonchain.contract import ContractBase
from moneyonchain.moc import CommissionSplitter


class RDOCCommissionSplitter(CommissionSplitter):

    contract_name = 'RDOCCommissionSplitter'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionSplitter.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionSplitter.bin'))

    mode = 'RDoC'
    precision = 10 ** 18

    def reserve_address(self, block_identifier: BlockIdentifier = 'latest'):
        """The reserve contract address"""

        result = self.sc.reserveToken(block_identifier=block_identifier)

        return result
