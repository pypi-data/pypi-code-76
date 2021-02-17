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

from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.governance import ProxyAdmin


class MoCSettlement(ContractBase):
    contract_name = 'MoCSettlement'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlement.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlement.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCSettlement']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.network_manager).from_abi()
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def next_block(self, block_identifier: BlockIdentifier = 'latest'):
        return int(self.sc.nextSettlementBlock(block_identifier=block_identifier))

    def is_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.isSettlementEnabled(block_identifier=block_identifier)

    def is_ready(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.isSettlementReady(block_identifier=block_identifier)

    def is_running(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.isSettlementRunning(block_identifier=block_identifier)

    def redeem_queue_size(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.redeemQueueSize(block_identifier=block_identifier)

    def block_span(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.getBlockSpan(block_identifier=block_identifier)
