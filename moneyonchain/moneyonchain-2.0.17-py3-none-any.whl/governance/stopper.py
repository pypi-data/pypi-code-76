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


class MoCStopper(ContractBase):

    contract_name = 'Stopper'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['stopper']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def address_stopper(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.stopper(block_identifier=block_identifier)

        return result

    def owner(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.owner(block_identifier=block_identifier)

        return result

    def pause(self,
              contract_to_pause,
              **tx_arguments):
        """pause"""

        contract_to_pause = Web3.toChecksumAddress(contract_to_pause)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.pause(contract_to_pause,
                                   tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def unpause(self,
                contract_to_pause,
                **tx_arguments):
        """unpause"""

        contract_to_pause = Web3.toChecksumAddress(contract_to_pause)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.unpause(
            contract_to_pause,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def transfer_ownership(self,
                           new_owner,
                           **tx_arguments):
        """
        function transferOwnership(address newOwner) public onlyOwner {
            _transferOwnership(newOwner);
        }
        """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.transferOwnership(Web3.toChecksumAddress(new_owner),
                                               tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt


class RDOCStopper(MoCStopper):
    log = logging.getLogger()
    contract_name = 'Stopper'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.bin'))

    mode = 'RDoC'
    precision = 10 ** 18
