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
import math

from moneyonchain.contract import ContractBase
from moneyonchain.moc import MoC, MoCConnector
from moneyonchain.transaction import receipt_to_log

from .mocinrate import VENDORSMoCInrate
from .mocstate import VENDORSMoCState
from .mocexchange import VENDORSMoCExchange
from .mocsettlement import VENDORSMoCSettlement
from .mocvendors import VENDORSMoCVendors

from moneyonchain.tokens import BProToken, DoCToken, MoCToken


STATE_LIQUIDATED = 0
STATE_BPRO_DISCOUNT = 1
STATE_BELOW_COBJ = 2
STATE_ABOVE_COBJ = 3

BUCKET_X2 = '0x5832000000000000000000000000000000000000000000000000000000000000'
BUCKET_C0 = '0x4330000000000000000000000000000000000000000000000000000000000000'


class VENDORSMoC(MoC):
    contract_name = 'MoC'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'
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
                 contract_address_moc_moc_token=None,
                 contract_address_moc_vendors=None,
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
            contract_addresses['MoCToken'] = contract_address_moc_moc_token
            contract_addresses['MoCVendors'] = contract_address_moc_vendors

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

        # load contract moc moc_token
        if contract_addresses['MoCToken']:
            self.sc_moc_moc_token = self.load_moc_moc_token_contract(contract_addresses['MoCToken'])
        else:
            self.sc_moc_moc_token = self.load_moc_moc_token_contract(self.sc_moc_state.moc_token())

        # load contract moc vendors
        if contract_addresses['MoCVendors']:
            self.sc_moc_vendors = self.load_moc_vendors_contract(contract_addresses['MoCVendors'])
        else:
            self.sc_moc_vendors = self.load_moc_vendors_contract(self.sc_moc_state.moc_vendors())

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
        contract_addresses['MoCToken'] = None
        contract_addresses['MoCVendors'] = None

        self.load_sub_contracts(contract_addresses)

        return self

    def load_moc_inrate_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        sc = VENDORSMoCInrate(self.network_manager,
                              contract_address=contract_address).from_abi()

        return sc

    def load_moc_state_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        sc = VENDORSMoCState(self.network_manager,
                             contract_address=contract_address).from_abi()

        return sc

    def load_moc_exchange_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCExchange']

        sc = VENDORSMoCExchange(self.network_manager,
                                contract_address=contract_address).from_abi()

        return sc

    def load_moc_connector_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCConnector']

        sc = MoCConnector(self.network_manager,
                          contract_address=contract_address).from_abi()

        return sc

    def load_moc_settlement_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCSettlement']

        sc = VENDORSMoCSettlement(self.network_manager,
                                  contract_address=contract_address).from_abi()

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['BProToken']

        sc = BProToken(self.network_manager,
                       contract_address=contract_address).from_abi()

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['DoCToken']

        sc = DoCToken(self.network_manager,
                      contract_address=contract_address).from_abi()

        return sc

    def load_moc_moc_token_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCToken']

        sc = MoCToken(self.network_manager,
                      contract_address=contract_address).from_abi()

        return sc

    def load_moc_vendors_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCVendors']

        sc = VENDORSMoCVendors(self.network_manager,
                               contract_address=contract_address).from_abi()

        return sc

    def moc_price(self,
                  formatted: bool = True,
                  block_identifier: BlockIdentifier = 'latest'):
        """MoC price in USD"""

        result = self.sc_moc_state.moc_price(
            formatted=formatted,
            block_identifier=block_identifier)

        return result

    def moc_balance_of(self,
                       account_address,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_moc_token.balance_of(
            account_address,
            formatted=formatted,
            block_identifier=block_identifier)

    def moc_allowance(self,
                      account_address,
                      contract_address,
                      formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_moc_token.allowance(
            account_address,
            contract_address,
            formatted=formatted,
            block_identifier=block_identifier)

    def mint_bpro_gas_estimated(self,
                                amount,
                                vendor_account,
                                precision=False,
                                **tx_arguments):

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintBProVendors.estimate_gas(int(amount), vendor_account, tx_args)
        else:
            return self.sc.mintRiskPro.estimate_gas(int(amount), tx_args)

    def mint_doc_gas_estimated(self,
                               amount,
                               vendor_account,
                               precision=False,
                               **tx_arguments):

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintDocVendors.estimate_gas(int(amount), vendor_account, tx_args)
        else:
            return self.sc.mintStableToken.estimate_gas(int(amount), tx_args)

    def mint_bprox_gas_estimated(self,
                                 amount,
                                 vendor_account,
                                 precision=False,
                                 **tx_arguments):

        bucket = BUCKET_X2

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintBProxVendors.estimate_gas(bucket, int(amount), vendor_account, tx_args)
        else:
            return self.sc.mintRiskProx.estimate_gas(bucket, int(amount), tx_args)

    def mint_bpro(self,
                  amount: Decimal,
                  vendor_account,
                  **tx_arguments):
        """ Mint amount bitpro
        NOTE: amount is in RBTC value
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        total_amount, commission_value, markup_value = self.amount_mint_bpro(amount, vendor_account, default_account)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        if self.mode != 'MoC':
            max_mint_bpro_available = self.max_mint_bpro_available()
            if total_amount >= max_mint_bpro_available:
                raise Exception("You are trying to mint more than the limit. Mint RiskPro limit: {0}".format(
                    max_mint_bpro_available))

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(total_amount * self.precision)

        tx_receipt = self.sc.mintBProVendors(
            int(amount * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def mint_doc(self,
                 amount: Decimal,
                 vendor_account,
                 **tx_arguments):
        """ Mint amount DOC
        NOTE: amount is in RBTC value
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if self.state() < STATE_ABOVE_COBJ:
            raise Exception("Function cannot be called at this state.")

        absolute_max_doc = self.absolute_max_doc()
        btc_to_doc = amount * self.bitcoin_price()
        if btc_to_doc > absolute_max_doc:
            raise Exception("You are trying to mint more than availables. DOC Avalaible: {0}".format(
                absolute_max_doc))

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        total_amount, commission_value, markup_value = self.amount_mint_doc(amount, vendor_account, default_account)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(total_amount * self.precision)

        tx_receipt = self.sc.mintDocVendors(
            int(amount * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def mint_btcx(self,
                  amount: Decimal,
                  vendor_account,
                  **tx_arguments):
        """ Mint amount BTC2X
        NOTE: amount is in RBTC value
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        max_bprox_btc_value = self.max_bprox_btc_value()
        if amount > max_bprox_btc_value:
            raise Exception("You are trying to mint more than availables. BTC2x available: {0}".format(
                max_bprox_btc_value))

        total_amount, commission_value, markup_value, interest_value = self.amount_mint_btc2x(amount, vendor_account,
                                                                                              default_account)
        bucket = BUCKET_X2

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(math.ceil(total_amount * self.precision))

        tx_receipt = self.sc.mintBProxVendors(
            bucket, int(amount * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_bpro(self,
                     amount_token: Decimal,
                     vendor_account,
                     **tx_arguments):
        """ Reedem BitPro amount of token """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if self.state() < STATE_ABOVE_COBJ:
            raise Exception("Function cannot be called at this state.")

        # get bpro balance
        if not default_account:
            default_account = 0
        account_address = self.network_manager.accounts[default_account].address
        if amount_token > self.bpro_balance_of(account_address):
            raise Exception("You are trying to redeem more than you have!")

        absolute_max_bpro = self.absolute_max_bpro()
        if amount_token >= absolute_max_bpro:
            raise Exception("You are trying to redeem more than availables. Available: {0}".format(
                absolute_max_bpro))

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.redeemBProVendors(
            int(amount_token * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_free_doc(self,
                         amount_token: Decimal,
                         vendor_account,
                         **tx_arguments):
        """
        Reedem Free DOC amount of token
        Free Doc is Doc you can reedeem outside of settlement.
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.network_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        free_doc = self.free_doc()
        if amount_token >= free_doc:
            raise Exception("You are trying to redeem more than availables. Available: {0}".format(
                free_doc))

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.redeemFreeDocVendors(
            int(amount_token * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_btc2x(self,
                      amount_token: Decimal,
                      vendor_account,
                      **tx_arguments):
        """ Reedem BTC2X amount of token """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot reedem on settlement!")

        # get bprox balance of
        if not default_account:
            default_account = 0
        account_address = self.network_manager.accounts[default_account].address
        account_balance = self.bprox_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! BTC2X Balance: {0}".format(account_balance))

        bucket = BUCKET_X2

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.redeemBProxVendors(
            bucket,
            int(amount_token * self.precision),
            vendor_account,
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_liquidation(self,
                            **tx_arguments):
        """Execute liquidation """

        tx_receipt = None
        if self.sc_moc_state.is_liquidation():

            self.log.info("Calling evalLiquidation ...")

            tx_args = self.tx_arguments(**tx_arguments)

            # Only if is liquidation reach
            tx_receipt = self.sc.evalLiquidation(
                tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def amount_mint_bpro(self,
                         amount: Decimal,
                         vendor_account,
                         default_account=None):
        """Final amount need it to mint bitpro in RBTC"""

        if not default_account:
            default_account = 0

        tx_type_fees_MOC = self.sc_moc_inrate.tx_type_mint_bpro_fees_moc()
        tx_type_fees_RBTC = self.sc_moc_inrate.tx_type_mint_bpro_fees_rbtc()

        commissions = self.sc_moc_exchange.calculate_commissions_with_prices(
            amount,
            tx_type_fees_MOC,
            tx_type_fees_RBTC,
            vendor_account,
            default_account=default_account)

        commission_value = commissions["btcCommission"]
        markup_value = commissions["btcMarkup"]
        total_amount = amount + commission_value + markup_value

        return total_amount, commission_value, markup_value

    def amount_mint_doc(self,
                        amount: Decimal,
                        vendor_account,
                        default_account=None):
        """Final amount need it to mint doc"""

        if not default_account:
            default_account = 0

        tx_type_fees_MOC = self.sc_moc_inrate.tx_type_mint_doc_fees_moc()
        tx_type_fees_RBTC = self.sc_moc_inrate.tx_type_mint_doc_fees_rbtc()

        commissions = self.sc_moc_exchange.calculate_commissions_with_prices(
            amount,
            tx_type_fees_MOC,
            tx_type_fees_RBTC,
            vendor_account,
            default_account=default_account)

        commission_value = commissions["btcCommission"]
        markup_value = commissions["btcMarkup"]
        total_amount = amount + commission_value + markup_value

        return total_amount, commission_value, markup_value

    def amount_mint_btc2x(self,
                          amount: Decimal,
                          vendor_account,
                          default_account=None):
        """Final amount need it to mint btc2x"""

        if not default_account:
            default_account = 0

        tx_type_fees_MOC = self.sc_moc_inrate.tx_type_mint_btcx_fees_moc()
        tx_type_fees_RBTC = self.sc_moc_inrate.tx_type_mint_btcx_fees_rbtc()

        commissions = self.sc_moc_exchange.calculate_commissions_with_prices(
            amount,
            tx_type_fees_MOC,
            tx_type_fees_RBTC,
            vendor_account,
            default_account=default_account)

        interest_value = self.sc_moc_inrate.calc_mint_interest_value(amount)

        commission_value = commissions["btcCommission"]
        markup_value = commissions["btcMarkup"]
        interest_value_margin = interest_value + interest_value * Decimal(0.01)
        total_amount = amount + commission_value + markup_value + interest_value_margin

        return total_amount, commission_value, markup_value, interest_value

