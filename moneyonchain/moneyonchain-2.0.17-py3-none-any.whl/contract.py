"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import json
import logging
from typing import (
    Optional
)
from web3.types import BlockIdentifier
from brownie import Contract

from moneyonchain.account import Account


class ContractBase(object):

    log = logging.getLogger()
    contract_name = 'Contract Name'
    contract_address = None
    contract_abi = None
    contract_bin = None
    sc = None
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None,
                 logger=None):

        self.network_manager = network_manager

        # Contract Name
        if contract_name:
            self.contract_name = contract_name

        # Contract address
        if contract_address:
            self.contract_address = contract_address

        # Contract abi
        if contract_abi:
            self.contract_abi = contract_abi

        # Contract bin
        if contract_bin:
            self.contract_bin = contract_bin

        if logger:
            self.log = logger

    def from_abi(self):
        self.sc = Contract.from_abi(self.contract_name, self.contract_address, self.contract_abi)
        return self

    def address(self):
        return self.sc.address

    def tx_arguments(self,
                     gas_limit=None,
                     gas_buffer=None,
                     gas_price=None,
                     amount=None,
                     nonce=None,
                     required_confs=1,
                     allow_revert=False,
                     default_account=None):

        tx_account = self.network_manager.accounts[self.network_manager.default_account]
        if default_account:
            tx_account = self.network_manager.accounts[default_account]

        d_tx = {
            "gas_limit": gas_limit,
            "gas_buffer": gas_buffer,
            "gas_price": gas_price,
            "amount": amount,
            "nonce": nonce,
            "required_confs": required_confs,
            "allow_revert": allow_revert,
            "from": tx_account
        }

        return d_tx

    def deploy(self,
               *args,
               default_account=None,
               **tx_arguments):
        """ Deploy contract """

        account_base = Account(self.network_manager,
                               default_account=default_account)
        receipt = account_base.deploy(self, *args, **tx_arguments)

        return receipt

    @staticmethod
    def content_abi_file(abi_file):

        with open(abi_file) as f:
            abi = json.load(f)

        return abi

    @staticmethod
    def content_bin_file(bin_file):

        with open(bin_file) as f:
            content_bin = f.read()

        return content_bin

    def load_abi_file(self, abi_file):

        self.contract_abi = self.content_abi_file(abi_file)

    def load_bin_file(self, bin_file):

        self.contract_bin = self.content_bin_file(bin_file)

    def filter_events(self,
                      from_block: Optional[BlockIdentifier] = None,
                      to_block: BlockIdentifier = "latest"
                      ):
        """ filter events """

        filter_params = {
            'fromBlock': from_block,
            'toBlock': to_block,
            'address': self.address()
        }

        return self.network_manager.filter_events(filter_params)

