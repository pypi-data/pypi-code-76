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


class PriceFeed(ContractBase):
    contract_name = 'PriceFeed'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeed.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeed.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None,
                 contract_address_moc_medianizer=None):

        config_network = network_manager.config_network
        if not contract_address:
            contract_address = network_manager.options['networks'][config_network]['addresses']['PriceFeed']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        if not contract_address_moc_medianizer:
            contract_address_moc_medianizer = network_manager.options['networks'][config_network]['addresses']['MoCMedianizer']

        self.contract_address_moc_medianizer = contract_address_moc_medianizer

    def post(self,
             p_price,
             block_expiration=300,
             **tx_arguments):
        """ Post price """

        address_moc_medianizer = Web3.toChecksumAddress(self.contract_address_moc_medianizer)
        last_block = self.network_manager.get_block('latest')
        expiration = last_block.timestamp + block_expiration

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.post(
            int(p_price),
            int(expiration),
            address_moc_medianizer,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return None, tx_receipt

    def zzz(self, block_identifier: BlockIdentifier = 'latest'):
        """zzz"""

        result = self.sc.zzz(block_identifier=block_identifier)

        return result

    def peek(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.peek(block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]


class RRC20PriceFeed(PriceFeed):

    contract_name = 'PriceFeed'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/PriceFeed.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/PriceFeed.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18


class RDOCPriceFeed(RRC20PriceFeed):

    contract_name = 'PriceFeed'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeed.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeed.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18
