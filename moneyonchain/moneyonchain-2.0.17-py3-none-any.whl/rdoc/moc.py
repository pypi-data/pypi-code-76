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
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.rrc20 import RRC20MoC
from moneyonchain.tokens import RIFPro, RIFDoC, RIF

from .mocinrate import RDOCMoCInrate
from .mocstate import RDOCMoCState
from .mocexchange import RDOCMoCExchange
from .mocconnector import RDOCMoCConnector
from .mocsettlement import RDOCMoCSettlement


class RDOCMoC(RRC20MoC):
    contract_name = 'MoC'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'
    minimum_amount = Decimal(0.00000001)

    def load_moc_inrate_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        sc = RDOCMoCInrate(self.network_manager,
                           contract_address=contract_address).from_abi()

        return sc

    def load_moc_state_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        sc = RDOCMoCState(self.network_manager,
                          contract_address=contract_address).from_abi()

        return sc

    def load_moc_exchange_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCExchange']

        sc = RDOCMoCExchange(self.network_manager,
                             contract_address=contract_address).from_abi()

        return sc

    def load_moc_connector_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCConnector']

        sc = RDOCMoCConnector(self.network_manager,
                              contract_address=contract_address).from_abi()

        return sc

    def load_moc_settlement_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCSettlement']

        sc = RDOCMoCSettlement(self.network_manager,
                               contract_address=contract_address).from_abi()

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['BProToken']

        sc = RIFPro(self.network_manager,
                    contract_address=contract_address).from_abi()

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['DoCToken']

        sc = RIFDoC(self.network_manager,
                    contract_address=contract_address).from_abi()

        return sc

    def load_reserve_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['ReserveToken']

        sc = RIF(self.network_manager,
                 contract_address=contract_address).from_abi()

        return sc

    def reserve_balance_of(self,
                           account_address,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):

        return self.sc_reserve_token.balance_of(account_address,
                                                formatted=formatted,
                                                block_identifier=block_identifier)
