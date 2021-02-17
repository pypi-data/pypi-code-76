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
from decimal import Decimal

from moneyonchain.contract import ContractBase
from .erc20 import ERC20Token


class WRBTCToken(ERC20Token):

    contract_name = 'WRBTC'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/WRBTCToken.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/WRBTCToken.bin'))

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['WRBTCToken']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def deposit(self,
                amount,
                **tx_arguments):
        """ Wrap """

        sc_amount = int(Decimal(amount) * self.precision)

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = sc_amount

        tx_receipt = self.sc.deposit(tx_args)

        tx_receipt.info()

        return tx_receipt

    def withdraw(self,
                 amount,
                 **tx_arguments):
        """ withdraw """

        sc_amount = int(Decimal(amount) * self.precision)

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.withdraw(sc_amount, tx_args)
        tx_receipt.info()

        return tx_receipt
