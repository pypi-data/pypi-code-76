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
from decimal import Decimal
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.governance import ProxyAdmin


class CommissionManager(ContractBase):

    contract_name = 'CommissionManager'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionManager.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionManager.bin'))
    mode = 'DEX'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['commissionManager']

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

    def beneficiary_address(self, block_identifier: BlockIdentifier = 'latest'):
        """Gets beneficiary destination address """

        result = self.sc.beneficiaryAddress(block_identifier=block_identifier)

        return result

    def commision_rate(self,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """Gets commision rate"""

        result = self.sc.commissionRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def minimum_commission(self,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """Get minimum commission"""

        result = self.sc.minimumCommission(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def cancelation_penalty_rate(self,
                                 formatted: bool = True,
                                 block_identifier: BlockIdentifier = 'latest'):
        """Gets cancelationPenaltyRate"""

        result = self.sc.cancelationPenaltyRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def expiration_penalty_rate(self,
                                formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """Gets expirationPenaltyRate"""

        result = self.sc.expirationPenaltyRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def calculate_initial_fee(self,
                              amount: float,
                              price: float,
                              formatted: bool = True,
                              block_identifier: BlockIdentifier = 'latest'):
        """Calculate initial fee. Initial fee is the commission at insertion order"""

        amount_sc = int(Decimal(amount) * self.precision)
        price_sc = int(Decimal(price) * self.precision)

        result = self.sc.calculateInitialFee(amount_sc, price_sc, block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def exchange_commissions(self,
                             address: str,
                             formatted: bool = True,
                             block_identifier: BlockIdentifier = 'latest'):
        """Gets exchangeCommissions"""

        result = self.sc.exchangeCommissions(Web3.toChecksumAddress(address), block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result
