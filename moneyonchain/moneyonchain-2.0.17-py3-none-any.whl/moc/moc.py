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
import datetime
from decimal import Decimal
from web3 import Web3
from web3.types import BlockIdentifier
import math

from moneyonchain.contract import ContractBase
from moneyonchain.transaction import receipt_to_log

from .mocinrate import MoCInrate
from .mocstate import MoCState
from .mocexchange import MoCExchange
from .mocconnector import MoCConnector
from .mocsettlement import MoCSettlement

from moneyonchain.tokens import BProToken, DoCToken
from moneyonchain.governance import ProxyAdmin


STATE_LIQUIDATED = 0
STATE_BPRO_DISCOUNT = 1
STATE_BELOW_COBJ = 2
STATE_ABOVE_COBJ = 3

BUCKET_X2 = '0x5832000000000000000000000000000000000000000000000000000000000000'
BUCKET_C0 = '0x4330000000000000000000000000000000000000000000000000000000000000'


class MoC(ContractBase):
    contract_name = 'MoC'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'
    minimum_amount = Decimal(0.00000001)
    receipt_timeout = 240
    poll_latency = 1.0

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
                 load_sub_contract=True
                 ):

        config_network = network_manager.config_network
        if not contract_address:
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoC']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        if load_sub_contract:
            contract_addresses = dict()
            contract_addresses['MoCState'] = contract_address_moc_state
            contract_addresses['MoCInrate'] = contract_address_moc_inrate
            contract_addresses['MoCExchange'] = contract_address_moc_exchange
            contract_addresses['MoCConnector'] = contract_address_moc_connector
            contract_addresses['MoCSettlement'] = contract_address_moc_settlement
            contract_addresses['BProToken'] = contract_address_moc_bpro_token
            contract_addresses['DoCToken'] = contract_address_moc_doc_token

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

        self.load_sub_contracts(contract_addresses)

        return self

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.network_manager).from_abi()
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def governor(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.governor(block_identifier=block_identifier)

        return result

    def load_moc_inrate_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        sc = MoCInrate(self.network_manager,
                       contract_address=contract_address).from_abi()

        return sc

    def load_moc_state_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        sc = MoCState(self.network_manager,
                      contract_address=contract_address).from_abi()

        return sc

    def load_moc_exchange_contract(self, contract_address):

        config_network = self.network_manager.config_network
        if not contract_address:
            contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCExchange']

        sc = MoCExchange(self.network_manager,
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

        sc = MoCSettlement(self.network_manager,
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

    def connector(self):

        return self.sc.connector()

    def connector_addresses(self):

        return self.sc_moc_connector.contracts_addresses()

    def state(self):

        return self.sc_moc_state.state()

    def reserve_precision(self,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Precision """

        result = self.sc.getReservePrecision(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def sc_precision(self,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """ Precision """

        result = self.sc.getMocPrecision(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def is_bucket_liquidation(self, block_identifier: BlockIdentifier = 'latest'):
        """Is bucket liquidation reached"""

        result = self.sc.isBucketLiquidationReached(BUCKET_X2, block_identifier=block_identifier)

        return result

    def is_settlement_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is settlement enabled"""

        result = self.sc.isSettlementEnabled(block_identifier=block_identifier)

        return result

    def is_daily_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is settlement enabled"""

        result = self.sc.isDailyEnabled(block_identifier=block_identifier)

        return result

    def is_bitpro_interest_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is bitpro_interest enabled"""

        if self.mode == 'MoC':
            result = self.sc.isBitProInterestEnabled(block_identifier=block_identifier)
        else:
            result = self.sc.isRiskProInterestEnabled(block_identifier=block_identifier)

        return result

    def execute_liquidation(self,
                            execution_steps,
                            **tx_arguments):
        """Execute liquidation """

        tx_receipt = None
        if self.sc_moc_state.is_liquidation():

            self.log.info("Calling evalLiquidation steps [{0}] ...".format(execution_steps))

            tx_args = self.tx_arguments(**tx_arguments)

            # Only if is liquidation reach
            tx_receipt = self.sc.evalLiquidation(
                execution_steps,
                tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_bucket_liquidation(self,
                                   **tx_arguments):
        """Execute bucket liquidation """

        tx_receipt = None
        if self.is_bucket_liquidation() and not self.is_settlement_enabled():

            self.log.info("Calling evalBucketLiquidation...")

            tx_args = self.tx_arguments(**tx_arguments)

            # Only if is liquidation reach
            tx_receipt = self.sc.evalBucketLiquidation(
                BUCKET_X2,
                tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_run_settlement(self,
                               execution_steps,
                               **tx_arguments):
        """Execute run settlement """

        tx_receipt = None
        if self.is_settlement_enabled():

            self.log.info("Calling runSettlement steps [{0}] ...".format(execution_steps))

            tx_args = self.tx_arguments(**tx_arguments)

            tx_receipt = self.sc.runSettlement(
                execution_steps,
                tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_daily_inrate_payment(self,
                                     **tx_arguments):
        """Execute daily inrate """

        tx_receipt = None
        if self.is_daily_enabled():

            self.log.info("Calling dailyInratePayment ...")

            tx_args = self.tx_arguments(**tx_arguments)

            tx_receipt = self.sc.dailyInratePayment(tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_pay_bitpro_holders(self,
                                   **tx_arguments):
        """Execute pay bitpro holders """

        tx_receipt = None
        if self.is_bitpro_interest_enabled():

            self.log.info("Calling payBitProHoldersInterestPayment ...")

            tx_args = self.tx_arguments(**tx_arguments)

            if self.mode == 'MoC':
                tx_receipt = self.sc.payBitProHoldersInterestPayment(tx_args)
            else:
                tx_receipt = self.sc.payRiskProHoldersInterestPayment(tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def execute_calculate_ema(self,
                              **tx_arguments):
        """Execute calculate ema """

        tx_receipt = self.sc_moc_state.execute_calculate_ema(
            **tx_arguments)

        return tx_receipt

    def max_mint_bpro_available(self):

        return self.sc_moc_state.max_mint_bpro_available()

    def absolute_max_doc(self):

        return self.sc_moc_state.absolute_max_doc()

    def max_bprox_btc_value(self):

        return self.sc_moc_state.max_bprox_btc_value()

    def absolute_max_bpro(self):

        return self.sc_moc_state.absolute_max_bpro()

    def free_doc(self):

        return self.sc_moc_state.free_doc()

    def settlement_info(self, avg_block_time=30.0):

        def convert(seconds):
            min, sec = divmod(seconds, 60)
            hour, min = divmod(min, 60)
            return "%d:%02d:%02d" % (hour, min, sec)

        blocks_to_settlement = self.sc_moc_state.blocks_to_settlement()

        l_sett = list()
        l_sett.append(('Current Block', int(self.network_manager.block_number)))
        l_sett.append(('Current avg block time (seconds)', 30.0))
        l_sett.append(('Blocks to settlement', blocks_to_settlement))
        l_sett.append(('Days to settlement', self.sc_moc_state.days_to_settlement()))

        remainin_estimated_seconds = avg_block_time * blocks_to_settlement
        estimated_time = datetime.datetime.now() + datetime.timedelta(seconds=remainin_estimated_seconds)

        l_sett.append(('Estimated remaining to settlement', convert(remainin_estimated_seconds)))
        l_sett.append(('Estimated settlement', estimated_time.strftime("%Y-%m-%d %H:%M:%S")))
        l_sett.append(('Next settlement block', self.sc_moc_settlement.next_block()))
        l_sett.append(('Is settlement enabled', self.sc_moc_settlement.is_enabled()))
        l_sett.append(('Is settlement ready', self.sc_moc_settlement.is_ready()))
        l_sett.append(('Is settlement running', self.sc_moc_settlement.is_running()))
        l_sett.append(('Reedem queue size', self.sc_moc_settlement.redeem_queue_size()))
        l_sett.append(('Block Span', self.sc_moc_settlement.block_span()))

        return l_sett

    def bitcoin_price(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin price in USD"""

        result = self.sc_moc_state.bitcoin_price(formatted=formatted,
                                                 block_identifier=block_identifier)

        return result

    def bpro_price(self,
                   formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """BPro price in USD"""

        result = self.sc_moc_state.bpro_price(formatted=formatted,
                                              block_identifier=block_identifier)

        return result

    def btc2x_tec_price(self,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """BTC2x price in USD"""

        result = self.sc_moc_state.btc2x_tec_price(formatted=formatted,
                                                   block_identifier=block_identifier)

        return result

    def bpro_amount_in_usd(self, amount: Decimal):

        return self.bpro_price() * amount

    def btc2x_amount_in_usd(self, amount: Decimal):

        return self.btc2x_tec_price() * self.bitcoin_price() * amount

    def balance_of(self, default_account=None):

        if not default_account:
            default_account = 0

        return self.network_manager.accounts[default_account].balance()

    def rbtc_balance_of(self,
                        account_address,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):

        result = self.network_manager.network_balance(account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def spendable_balance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Compatibility function see RRC20 """

        result = self.network_manager.network_balance(account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def reserve_allowance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Compatibility function see RRC20 """

        result = self.network_manager.network_balance(account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_balance_of(self,
                       account_address,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_doc_token.balance_of(account_address,
                                                formatted=formatted,
                                                block_identifier=block_identifier)

    def bpro_balance_of(self,
                        account_address,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_bpro_token.balance_of(account_address,
                                                 formatted=formatted,
                                                 block_identifier=block_identifier)

    def bprox_balance_of(self,
                         account_address,
                         formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):

        bucket = BUCKET_X2

        if self.mode == 'MoC':
            result = self.sc.bproxBalanceOf(bucket, account_address, block_identifier=block_identifier)
        else:
            result = self.sc.riskProxBalanceOf(bucket, account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_amount_to_redeem(self,
                             account_address,
                             formatted: bool = True,
                             block_identifier: BlockIdentifier = 'latest'):

        if self.mode == 'MoC':
            result = self.sc.docAmountToRedeem(account_address, block_identifier=block_identifier)
        else:
            result = self.sc.stableTokenAmountToRedeem(account_address, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def paused(self,
               block_identifier: BlockIdentifier = 'latest'):
        """is Paused"""

        result = self.sc.paused(block_identifier=block_identifier)

        return result

    def stoppable(self,
                  block_identifier: BlockIdentifier = 'latest'):
        """is Paused"""

        result = self.sc.stoppable(block_identifier=block_identifier)

        return result

    def stopper(self,
                block_identifier: BlockIdentifier = 'latest'):
        """is Paused"""

        result = self.sc.stopper(block_identifier=block_identifier)

        return result

    def amount_mint_bpro(self, amount: Decimal):
        """Final amount need it to mint bitpro in RBTC"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        total_amount = amount + commission_value

        return total_amount, commission_value

    def amount_mint_doc(self, amount: Decimal):
        """Final amount need it to mint doc"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        total_amount = amount + commission_value

        return total_amount, commission_value

    def amount_mint_btc2x(self, amount: Decimal):
        """Final amount need it to mint btc2x"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        interest_value = self.sc_moc_inrate.calc_mint_interest_value(amount)
        interest_value_margin = interest_value + interest_value * Decimal(0.01)
        total_amount = amount + commission_value + interest_value_margin

        return total_amount, commission_value, interest_value

    def mint_bpro_gas_estimated(self,
                                amount,
                                precision=False,
                                **tx_arguments):

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintBPro.estimate_gas(int(amount), tx_args)
        else:
            return self.sc.mintRiskPro.estimate_gas(int(amount), tx_args)

    def mint_doc_gas_estimated(self,
                               amount,
                               precision=False,
                               **tx_arguments):

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintDoc.estimate_gas(int(amount), tx_args)
        else:
            return self.sc.mintStableToken.estimate_gas(int(amount), tx_args)

    def mint_bprox_gas_estimated(self,
                                 amount,
                                 precision=False,
                                 **tx_arguments):

        bucket = BUCKET_X2

        if precision:
            amount = amount * self.precision

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            return self.sc.mintBProx.estimate_gas(bucket, int(amount), tx_args)
        else:
            return self.sc.mintRiskProx.estimate_gas(bucket, int(amount), tx_args)

    def mint_bpro(self,
                  amount: Decimal,
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

        total_amount, commission_value = self.amount_mint_bpro(amount)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        max_mint_bpro_available = self.max_mint_bpro_available()
        if total_amount >= max_mint_bpro_available:
            raise Exception("You are trying to mint more than the limit. Mint BPro limit: {0}".format(
                max_mint_bpro_available))

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(total_amount * self.precision)

        tx_receipt = self.sc.mintBPro(
            int(amount * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def mint_doc(self,
                 amount: Decimal,
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

        total_amount, commission_value = self.amount_mint_doc(amount)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(total_amount * self.precision)

        tx_receipt = self.sc.mintDoc(
            int(amount * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def mint_btcx(self,
                   amount: Decimal,
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
            raise Exception("You are trying to mint more than availables. BTCx available: {0}".format(
                max_bprox_btc_value))

        total_amount, commission_value, interest_value = self.amount_mint_btc2x(amount)
        bucket = BUCKET_X2

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_args = self.tx_arguments(**tx_arguments)
        tx_args['amount'] = int(math.ceil(total_amount * self.precision))

        tx_receipt = self.sc.mintBProx(
            bucket, int(amount * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_bpro(self,
                     amount_token: Decimal,
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

        tx_receipt = self.sc.redeemBPro(
            int(amount_token * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_free_doc(self,
                         amount_token: Decimal,
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

        tx_receipt = self.sc.redeemFreeDoc(
            int(amount_token * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_doc_request(self,
                            amount_token: Decimal,
                            **tx_arguments):
        """
        Reedem DOC request amount of token
        This is the amount of doc you want to reedem on settlement.
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.network_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.redeemDocRequest(
            int(amount_token * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_doc_request_alter(self,
                                  amount_token: Decimal,
                                  **tx_arguments):
        """
        Redeeming DOCs on Settlement: alterRedeemRequestAmount

        There is only at most one redeem request per user during a settlement. A new redeem request is created
        if the user invokes it for the first time or updates its value if it already exists.
        """

        if 'default_account' in tx_arguments:
            default_account = tx_arguments['default_account']
        else:
            default_account = None

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.network_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.alterRedeemRequestAmount(
            int(amount_token * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def reedeem_btc2x(self,
                      amount_token: Decimal,
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

        tx_receipt = self.sc.redeemBProx(
            bucket,
            int(amount_token * self.precision),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def redeem_all_doc(self,
                       **tx_arguments):
        """
        Redeem All doc only on liquidation
        """

        tx_args = self.tx_arguments(**tx_arguments)

        if self.mode == 'MoC':
            tx_receipt = self.sc.redeemAllDoc(tx_args)
        else:
            tx_receipt = self.sc.redeemAllStableToken(tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

"""
    def search_block_transaction(self, block):

        network = self.connection_manager.network
        moc_addresses = list()
        moc_addresses.append(
            str.lower(self.connection_manager.options['networks'][network]['addresses']['MoC']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['MoCExchange']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['BProToken']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['DoCToken']))

        print(moc_addresses)

        l_transactions = list()
        f_block = self.connection_manager.get_block(block, full_transactions=True)
        for transaction in f_block['transactions']:
            if str.lower(transaction['to']) in moc_addresses or \
                    str.lower(transaction['from']) in moc_addresses:
                l_transactions.append(transaction)

        #transaction_receipt = node_manager.web3.eth.getTransactionReceipt(transaction)

        return l_transactions
"""
