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
import logging

from web3.types import BlockIdentifier
from web3 import Web3
from moneyonchain.contract import ContractBase
from moneyonchain.transaction import receipt_to_log


class Governed(ContractBase):

    contract_name = 'Governed'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        config_network = network_manager.config_network
        if not contract_address:
            raise ValueError("You need to pass contract address")

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def governor(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.governor(block_identifier=block_identifier)

        return result

    def initialize(self,
                   governor,
                   **tx_arguments):
        """Initialize"""

        governor_address = Web3.toChecksumAddress(governor)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.initialize(governor_address, tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt


class RDOCGoverned(Governed):
    log = logging.getLogger()
    contract_name = 'Governed'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.bin'))

    mode = 'RDoC'
    precision = 10 ** 18
