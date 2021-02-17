"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import logging
from typing import Optional, Tuple

from brownie import web3
from brownie.convert import Wei
from brownie.network.account import Account as _Account
#from brownie.network.state import Chain


from moneyonchain.transaction import TransactionReceipt
from moneyonchain.main import chain, accounts


class Account(_Account):

    log = logging.getLogger()

    def __init__(self,
                 network_manager,
                 default_account=None
                 ):

        self.network_manager = network_manager

        try:
            account = accounts[self.network_manager.default_account]
            if default_account:
                account = accounts[default_account]
        except ValueError:
            raise Exception("You need an account to deploy a contract!")

        self.account = account
        super().__init__(account.address)

    def deploy(self,
               contract,
               *args: Tuple,
               amount: int = 0,
               gas_limit: Optional[int] = 5500000,
               gas_buffer: Optional[float] = None,
               gas_price: Optional[int] = None,
               nonce: Optional[int] = None,
               required_confs: int = 1,
               allow_revert: bool = None,
               silent: bool = None):
        """ Deploy contract """

        #chain = Chain()

        if gas_limit and gas_buffer:
            raise ValueError("Cannot set gas_limit and gas_buffer together")

        gas_price, gas_strategy, gas_iter = self._gas_price(gas_price)
        gas_limit = Wei(gas_limit) or self._gas_limit(
            None, amount, gas_price, gas_buffer
        )

        sc = web3.eth.contract(abi=contract.contract_abi, bytecode=contract.contract_bin)
        built_fxn = sc.constructor(*args)

        transaction_dict = {'chainId': chain.id,
                            'nonce': nonce if nonce is not None else self._pending_nonce(),
                            'gasPrice': gas_price,
                            'gas': gas_limit}

        transaction = built_fxn.buildTransaction(transaction_dict)

        signed = web3.eth.account.signTransaction(transaction,
                                                  private_key=self.account.private_key)

        txid = web3.eth.sendRawTransaction(
            signed.rawTransaction)

        receipt = TransactionReceipt(
            txid,
            self,
            silent=silent,
            required_confs=required_confs,
            is_blocking=False,
            name=contract.contract_name
        )

        receipt = self._await_confirmation(receipt, required_confs, gas_strategy, gas_iter)

        return receipt
