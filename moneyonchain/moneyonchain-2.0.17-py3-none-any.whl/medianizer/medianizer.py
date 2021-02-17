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
from moneyonchain.transaction import receipt_to_log


class MoCMedianizer(ContractBase):

    contract_name = 'MoCDecentralizedExchange'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.bin'))

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
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCMedianizer']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def price(self, formatted: bool = True,
              block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.peek(block_identifier=block_identifier)

        if not result[1]:
            raise Exception("No source value price")

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price

    def min(self, block_identifier: BlockIdentifier = 'latest'):
        """ Min """

        result = self.sc.min(block_identifier=block_identifier)

        return result

    def set_min(self,
                minimum,
                **tx_arguments):
        """ Minimum price feeder """

        tx_receipt = self.sc.setMin(int(minimum), **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return None, tx_receipt

    def peek(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.peek(block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]

    def compute(self, formatted: bool = True,
                block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.compute(block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]

    def indexes(self, feeder_address,
                block_identifier: BlockIdentifier = 'latest'):
        """Get index of the price feeder. Result > 0 is an active pricefeeder"""

        feeder_address = Web3.toChecksumAddress(feeder_address)

        result = self.sc.indexes(feeder_address, block_identifier=block_identifier)

        return Web3.toInt(result)

    def poke(self,
             **tx_arguments):
        """ Poke """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.poke(tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return None, tx_receipt


class RRC20MoCMedianizer(MoCMedianizer):

    contract_name = 'MoCMedianizer'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCMedianizer.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCMedianizer.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18


class RDOCMoCMedianizer(RRC20MoCMedianizer):

    contract_name = 'MoCMedianizer'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18
