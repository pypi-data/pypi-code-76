"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging
from web3 import Web3
from web3.types import BlockIdentifier
from decimal import Decimal

from moneyonchain.contract import ContractBase


class ERC20Token(ContractBase):

    contract_name = 'ERC20Token'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def name(self):
        return self.sc.name()

    def symbol(self):
        return self.sc.symbol()

    def total_supply(self,
                     formatted=True,
                     block_identifier: BlockIdentifier = 'latest'):
        total = self.sc.totalSupply(block_identifier=block_identifier)
        if formatted:
            total = Web3.fromWei(total, 'ether')
        return total

    def balance_of(self,
                   account_address,
                   formatted=True,
                   block_identifier: BlockIdentifier = 'latest'):

        account_address = Web3.toChecksumAddress(account_address)

        balance = self.sc.balanceOf(account_address, block_identifier=block_identifier)
        if formatted:
            balance = Web3.fromWei(balance, 'ether')
        return balance

    def allowance(self,
                  account_address,
                  contract_address,
                  formatted=True,
                  block_identifier: BlockIdentifier = 'latest'):

        account_address = Web3.toChecksumAddress(account_address)
        contract_address = Web3.toChecksumAddress(contract_address)

        balance = self.sc.allowance(account_address,
                                    contract_address,
                                    block_identifier=block_identifier)
        if formatted:
            balance = Web3.fromWei(balance, 'ether')
        return balance

    def approve(self,
                contract_address,
                contract_amount,
                **tx_arguments
                ):
        """ Set allowance """

        sc_amount = int(Decimal(contract_amount) * self.precision)
        sc_address = Web3.toChecksumAddress(contract_address)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.approve(sc_address, sc_amount, tx_args)

        tx_receipt.info()

        return tx_receipt
