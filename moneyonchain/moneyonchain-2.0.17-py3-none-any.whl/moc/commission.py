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
from web3 import Web3
from moneyonchain.contract import ContractBase
from moneyonchain.transaction import receipt_to_log


class CommissionSplitter(ContractBase):
    contract_name = 'CommissionSplitter'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionSplitter.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionSplitter.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['CommissionSplitter']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def commission_address(self, block_identifier: BlockIdentifier = 'latest'):
        """Final receiver address"""

        result = self.sc.commissionsAddress(block_identifier=block_identifier)

        return result

    def moc_address(self, block_identifier: BlockIdentifier = 'latest'):
        """The MOC contract address"""

        result = self.sc.moc(block_identifier=block_identifier)

        return result

    def moc_proportion(self, block_identifier: BlockIdentifier = 'latest'):
        """ Proportion of the balance to send to moc """

        result = self.sc.mocProportion(block_identifier=block_identifier)

        return result

    def balance(self,
                formatted: bool = True,
                block_identifier: BlockIdentifier = 'latest'):

        #result = self.sc.balance(self.address(), block_identifier=block_identifier)
        result = self.network_manager.network_balance(self.address(), block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def initialize(self,
                   moc_address,
                   commission_address,
                   moc_proportion,
                   governor_address,
                   **tx_arguments):
        """Init the contract"""

        moc_address = Web3.toChecksumAddress(moc_address)
        commission_address = Web3.toChecksumAddress(commission_address)
        governor_address = Web3.toChecksumAddress(governor_address)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.initialize(
            moc_address,
            commission_address,
            moc_proportion,
            governor_address,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def split(self,
              **tx_arguments):
        """ split execute """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.split(tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt
