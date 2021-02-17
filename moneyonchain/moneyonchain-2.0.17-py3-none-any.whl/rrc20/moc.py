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
from moneyonchain.moc import MoC

from .mocinrate import RRC20MoCInrate
from .mocstate import RRC20MoCState
from .mocexchange import RRC20MoCExchange
from .mocconnector import RRC20MoCConnector
from .mocsettlement import RRC20MoCSettlement

from moneyonchain.tokens import RiskProToken, StableToken, ReserveToken


class RRC20MoC(MoC):
    contract_name = 'MoC'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'
    minimum_amount = Decimal(0.00000001)

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None,
                 contract_address_moc_state=None,
                 contract_address_moc_inrate=None,
                 contract_address_moc_exchange=None,
                 contract_address_moc_connector=None,
                 contract_address_moc_settlement=None,
                 contract_address_moc_bpro_token=None,
                 contract_address_moc_doc_token=None,
                 contract_address_reserve_token=None,
                 load_sub_contract=True):

        config_network = network_manager.config_network
        if not contract_address:
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoC']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin,
                         contract_address_moc_state=contract_address_moc_state,
                         contract_address_moc_inrate=contract_address_moc_inrate,
                         contract_address_moc_exchange=contract_address_moc_exchange,
                         contract_address_moc_connector=contract_address_moc_connector,
                         contract_address_moc_settlement=contract_address_moc_settlement,
                         contract_address_moc_bpro_token=contract_address_moc_bpro_token,
                         contract_address_moc_doc_token=contract_address_moc_doc_token,
                         load_sub_contract=False
                         )

        if load_sub_contract:
            contract_addresses = dict()
            contract_addresses['MoCState'] = contract_address_moc_state
            contract_addresses['MoCInrate'] = contract_address_moc_inrate
            contract_addresses['MoCExchange'] = contract_address_moc_exchange
            contract_addresses['MoCConnector'] = contract_address_moc_connector
            contract_addresses['MoCSettlement'] = contract_address_moc_settlement
            contract_addresses['BProToken'] = contract_address_moc_bpro_token
            contract_addresses['DoCToken'] = contract_address_moc_doc_token
            contract_addresses['ReserveToken'] = contract_address_reserve_token

            # load contract addresses
            self.load_sub_contracts(contract_addresses)

    def load_sub_contracts(self, contract_addresses):

        # load contract moc connector
        self.sc_moc_connector = self.load_moc_connector_contract(contract_addresses['MoCConnector'])

        # load contract moc state
        self.sc_moc_state = self.load_moc_state_contract(contract_addresses['MoCState'])

        # load contract moc inrate
        self.sc_moc_inrate = self.load_moc_inrate_contract(contract_addresses['MoCInrate'])

        # load contract moc exchange
        self.sc_moc_exchange = self.load_moc_exchange_contract(contract_addresses['MoCExchange'])

        # load contract moc settlement
        self.sc_moc_settlement = self.load_moc_settlement_contract(contract_addresses['MoCSettlement'])

        # load contract moc bpro_token
        self.sc_moc_bpro_token = self.load_moc_bpro_token_contract(contract_addresses['BProToken'])

        # load contract moc doc_token
        self.sc_moc_doc_token = self.load_moc_doc_token_contract(contract_addresses['DoCToken'])

        # load_reserve_token_contract
        self.sc_reserve_token = self.load_reserve_token_contract(contract_addresses['ReserveToken'])

    def contracts_discovery(self):
        """ This implementation get sub contracts only with MoC Contract address"""

        contract_addresses = dict()
        contract_addresses['MoCConnector'] = self.connector()
        self.sc_moc_connector = self.load_moc_connector_contract(contract_addresses['MoCConnector'])
        connector_addresses = self.connector_addresses()
        contract_addresses['MoCState'] = connector_addresses['MoCState']
        contract_addresses['MoCInrate'] = connector_addresses['MoCInrate']
        contract_addresses['MoCExchange'] = connector_addresses['MoCExchange']
        contract_addresses['MoCSettlement'] = connector_addresses['MoCSettlement']
        contract_addresses['BProToken'] = connector_addresses['BProToken']
        contract_addresses['DoCToken'] = connector_addresses['DoCToken']
        contract_addresses['ReserveToken'] = connector_addresses['ReserveToken']

        self.load_sub_contracts(contract_addresses)

        return self

    def load_moc_inrate_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        sc = RRC20MoCInrate(self.network_manager,
                            contract_address=contract_address).from_abi()

        return sc

    def load_moc_state_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        sc = RRC20MoCState(self.network_manager,
                           contract_address=contract_address).from_abi()

        return sc

    def load_moc_exchange_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCExchange']

        sc = RRC20MoCExchange(self.network_manager,
                              contract_address=contract_address).from_abi()

        return sc

    def load_moc_connector_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCConnector']

        sc = RRC20MoCConnector(self.network_manager,
                               contract_address=contract_address).from_abi()

        return sc

    def load_moc_settlement_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCSettlement']

        sc = RRC20MoCSettlement(self.network_manager,
                                contract_address=contract_address).from_abi()

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['BProToken']

        sc = RiskProToken(self.network_manager,
                          contract_address=contract_address).from_abi()

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['DoCToken']

        sc = StableToken(self.network_manager,
                         contract_address=contract_address).from_abi()

        return sc

    def load_reserve_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['ReserveToken']

        sc = ReserveToken(self.network_manager,
                          contract_address=contract_address).from_abi()

        return sc

    def spendable_balance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Spendable Balance """

        result = self.sc.getAllowance(account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def reserve_allowance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Reserve allowance """

        result = self.sc_reserve_token.allowance(account_address,
                                                 self.sc.address,
                                                 formatted=formatted,
                                                 block_identifier=block_identifier)

        return result

