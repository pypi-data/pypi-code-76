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
import logging
from decimal import Decimal
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.governance import ProxyAdmin
from moneyonchain.transaction import receipt_to_log


class MoCDecentralizedExchange(ContractBase):

    contract_name = 'MoCDecentralizedExchange'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCDecentralizedExchange.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCDecentralizedExchange.bin'))
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
            contract_address = network_manager.options['networks'][config_network]['addresses']['dex']

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

    def paused(self,
               block_identifier: BlockIdentifier = 'latest'):
        """is Paused"""

        result = self.sc.paused(block_identifier=block_identifier)

        return result

    def min_order_amount(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """Gets min order amount"""

        result = self.sc.minOrderAmount(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_order_lifespan(self, block_identifier: BlockIdentifier = 'latest'):
        """Is the maximum lifespan in ticks for an order

        @:return Integer number of max order lifespan in ticks
        """

        result = self.sc.maxOrderLifespan(block_identifier=block_identifier)

        return result

    def min_multiply_factor(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """ Minimum range avalaible price to be paid   """

        result = self.sc.minMultiplyFactor(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_multiply_factor(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """ Maximum range avalaible price to be paid   """

        result = self.sc.maxMultiplyFactor(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def token_pairs(self, block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        result = self.sc.getTokenPairs(block_identifier=block_identifier)

        return result

    def token_pairs_status(self, base_address, secondary_address,
                           block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        base_address = Web3.toChecksumAddress(base_address)
        secondary_address = Web3.toChecksumAddress(secondary_address)

        result = self.sc.getTokenPairStatus(base_address,
                                            secondary_address,
                                            block_identifier=block_identifier)

        if result:
            d_status = dict()
            d_status['emergentPrice'] = result[0]
            d_status['lastBuyMatchId'] = result[1]
            d_status['lastBuyMatchAmount'] = result[2]
            d_status['lastSellMatchId'] = result[3]
            d_status['tickNumber'] = result[4]
            d_status['nextTickBlock'] = result[5]
            d_status['lastTickBlock'] = result[6]
            d_status['lastClosingPrice'] = result[7]
            d_status['disabled'] = result[8]
            d_status['EMAPrice'] = result[9]
            d_status['smoothingFactor'] = result[10]
            d_status['marketPrice'] = result[11]

            return d_status

        return result

    def convert_token_to_common_base(self,
                                     token_address,
                                     amount,
                                     base_address,
                                     formatted: bool = True,
                                     block_identifier: BlockIdentifier = 'latest'):
        """
        @dev simple converter from the given token to a common base, in this case, Dollar on Chain
        @param token_address the token address of token to convert into the common base token
        @param amount the amount to convert
        @param base_address the address of the base of the pair in witch the token its going to operate.
        if the the token it is allready the base of the pair, this parameter it is unimportant
        @return convertedAmount the amount converted into the common base token
        """

        token_address = Web3.toChecksumAddress(token_address)
        base_address = Web3.toChecksumAddress(base_address)

        result = self.sc.convertTokenToCommonBase(token_address,
                                                  amount,
                                                  base_address,
                                                  block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def get_price_provider(self, base_address, secondary_address,
                           block_identifier: BlockIdentifier = 'latest'):
        """Returns the price provider of a given pair """

        base_address = Web3.toChecksumAddress(base_address)
        secondary_address = Web3.toChecksumAddress(secondary_address)

        result = self.sc.getPriceProvider(base_address,
                                          secondary_address,
                                          block_identifier=block_identifier)

        return result

    def next_tick(self, pair, block_identifier: BlockIdentifier = 'latest'):
        """ Next tick """

        result = self.sc.getNextTick(pair[0], pair[1], block_identifier=block_identifier)

        return result

    def are_orders_to_expire(self,
                             pair,
                             is_buy_order,
                             block_identifier: BlockIdentifier = 'latest'):
        """ Are orders to expire """

        result = self.sc.areOrdersToExpire(pair[0],
                                           pair[1],
                                           is_buy_order,
                                           block_identifier=block_identifier)

        return result

    def emergent_price(self,
                       pair,
                       block_identifier: BlockIdentifier = 'latest'):
        """ Calculates closing price as if the tick closes at this moment.
            emergentPrice: AVG price of the last matched Orders

            return (emergentPrice, lastBuyMatch.id, lastBuyMatch.exchangeableAmount, lastSellMatch.id);
            """

        result = self.sc.getEmergentPrice(
            pair[0],
            pair[1],
            block_identifier=block_identifier)
        return result

    def market_price(self,
                     pair,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """ Get the current market price """

        result = self.sc.getMarketPrice(pair[0],
                                        pair[1],
                                        block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def last_closing_price(self,
                           pair,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Getter for every value related to a pair
        _baseToken Address of the base token of the pair
        _secondaryToken Address of the secondary token of the pair
        lastClosingPrice - the last price from a successful matching
        """

        result = self.sc.getLastClosingPrice(
            pair[0],
            pair[1],
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def tick_is_running(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        notice Returns true if the pair is running a tick
        param _baseToken Address of the base token of the pair
        param _secondaryToken Address of the secondary token of the pair
        """

        result = self.sc.tickIsRunning(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def tick_stage(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        notice Returns the tick stage for a given pair
        param _baseToken Address of the base token of the pair
        param _secondaryToken Address of the secondary token of the pair
        return Enum representing the tick stage
        """

        result = self.sc.getTickStage(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def sell_orders_length(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Returns the amount of sell orders(not including the pending ones) that are in the orderbook of this pair
        param _baseToken the base token of the pair
        param _secondaryToken the secondary token of the pair
        """

        result = self.sc.sellOrdersLength(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def buy_orders_length(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Returns the amount of buy orders(not including the pending ones)
        that are in the orderbook of this pair
        param _baseToken the base token of the pair
        param _secondaryToken the secondary token of the pair
        """

        result = self.sc.buyOrdersLength(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def pending_sell_orders_length(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Returns the amount of pending sell orders that are in the orderbook of this pair
        that are in the orderbook of this pair
        param _baseToken the base token of the pair
        param _secondaryToken the secondary token of the pair
        """

        result = self.sc.pendingSellOrdersLength(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def pending_buy_orders_length(
            self,
            pair,
            block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Returns the amount of pending buy orders that are in the orderbook of this pair
        that are in the orderbook of this pair
        param _baseToken the base token of the pair
        param _secondaryToken the secondary token of the pair
        """

        result = self.sc.pendingBuyOrdersLength(
            pair[0],
            pair[1],
            block_identifier=block_identifier)

        return result

    def pending_market_orders_length(
            self,
            pair,
            is_buy=False,
            block_identifier: BlockIdentifier = 'latest'):
        """
        @notice Returns the amount of pending market orders that are in the orderbook of this pair
        param _baseToken the base token of the pair
        param _secondaryToken the secondary token of the pair
        param _isBuy true to get buy market orders amount, false to get sell market orders amount.
        """

        result = self.sc.pendingMarketOrdersLength(
            pair[0],
            pair[1],
            is_buy,
            block_identifier=block_identifier)

        return result

    def run_tick_for_pair(self,
                          pair,
                          matching_steps=70,
                          **tx_arguments):
        """Run tick for pair """

        tx_hash = None
        tx_receipt = None

        block_number = self.network_manager.block_number
        self.log.info('About to run tick for pair {0}'.format(pair))
        next_tick_info = self.next_tick(pair)
        block_of_next_tick = next_tick_info[1]

        self.log.info('BlockOfNextTick {0}, currentBlockNumber {1}'.format(
            block_of_next_tick, block_number))
        self.log.info('Is tick runnable? {0}'.format(
            block_of_next_tick <= block_number))
        if block_of_next_tick <= block_number:

            tx_args = self.tx_arguments(**tx_arguments)

            tx_receipt = self.sc.matchOrders(
                pair[0],
                pair[1],
                matching_steps,
                tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        else:
            self.log.info('Block of next tick has not been reached\n\n')

        return tx_hash, tx_receipt

    def run_orders_expiration_for_pair(self,
                                       pair,
                                       is_buy_order,
                                       order_type,
                                       hint=0,
                                       order_id=0,
                                       matching_steps=70,
                                       **tx_arguments):
        """Run order expiration """

        tx_hash = None
        block_number = self.network_manager.block_number

        self.log.info('About to expire {0} orders for pair {1} in blockNumber {2}'.format('buy' if is_buy_order else 'sell',
                                                                                          pair, block_number))

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.processExpired(pair[0],
                                            pair[1],
                                            is_buy_order,
                                            hint,
                                            order_id,
                                            matching_steps,
                                            order_type,
                                            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_hash, tx_receipt

    def _insert_sell_limit_order(self,
                                 base_token,
                                 secondary_token,
                                 amount,
                                 price,
                                 lifespan,
                                 **tx_arguments):
        """ Inserts an order in the sell orderbook of a given pair without a hint
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.insertSellLimitOrder(
            base_token,
            secondary_token,
            amount,
            price,
            lifespan,
            tx_args)

        return tx_receipt

    def insert_sell_limit_order(self,
                                base_token,
                                secondary_token,
                                amount,
                                price,
                                lifespan,
                                **tx_arguments):
        """ Inserts an order in the sell orderbook of a given pair without a hint
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)
        amount_sc = int(Decimal(amount) * self.precision)
        price_sc = int(Decimal(price) * self.precision)
        lifespan_sc = int(lifespan)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._insert_sell_limit_order(
            base_token,
            secondary_token,
            amount_sc,
            price_sc,
            lifespan_sc,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def _insert_buy_limit_order(self,
                                base_token,
                                secondary_token,
                                amount,
                                price,
                                lifespan,
                                **tx_arguments):
        """ @notice Inserts an order in the buy orderbook of a given pair without a hint
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.insertBuyLimitOrder(
            base_token,
            secondary_token,
            amount,
            price,
            lifespan,
            tx_args)

        return tx_receipt

    def insert_buy_limit_order(self,
                               base_token,
                               secondary_token,
                               amount,
                               price,
                               lifespan,
                               **tx_arguments):
        """ Inserts an order in the buy orderbook of a given pair without a hint
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)
        amount_sc = int(Decimal(amount) * self.precision)
        price_sc = int(Decimal(price) * self.precision)
        lifespan_sc = int(lifespan)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._insert_buy_limit_order(
            base_token,
            secondary_token,
            amount_sc,
            price_sc,
            lifespan_sc,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def _insert_sell_market_order(self,
                                  base_token,
                                  secondary_token,
                                  amount,
                                  multiply_factor,
                                  lifespan,
                                  **tx_arguments):
        """ Inserts a market order at start in the buy orderbook of a given pair with a hint;
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        is_buy = False

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.insertMarketOrder(
            base_token,
            secondary_token,
            amount,
            multiply_factor,
            lifespan,
            is_buy,
            tx_args)

        return tx_receipt

    def insert_sell_market_order(self,
                                 base_token,
                                 secondary_token,
                                 amount,
                                 multiply_factor,
                                 lifespan,
                                 **tx_arguments):
        """  Inserts a market order at start in the buy orderbook of a given pair with a hint;
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)
        amount_sc = int(Decimal(amount) * self.precision)
        multiply_factor_sc = int(Decimal(multiply_factor) * self.precision)
        lifespan_sc = int(lifespan)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._insert_sell_market_order(
            base_token,
            secondary_token,
            amount_sc,
            multiply_factor_sc,
            lifespan_sc,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def _insert_buy_market_order(self,
                                 base_token,
                                 secondary_token,
                                 amount,
                                 multiply_factor,
                                 lifespan,
                                 **tx_arguments):
        """ Inserts a market order at start in the buy orderbook of a given pair with a hint;
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        is_buy = True

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.insertMarketOrder(
            base_token,
            secondary_token,
            amount,
            multiply_factor,
            lifespan,
            is_buy,
            tx_args)

        return tx_receipt

    def insert_buy_market_order(self,
                                base_token,
                                secondary_token,
                                amount,
                                multiply_factor,
                                lifespan,
                                **tx_arguments):
        """  Inserts a market order at start in the buy orderbook of a given pair with a hint;
    the pair should not be disabled; the contract should not be paused. Takes the funds
    with a transferFrom """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)
        amount_sc = int(Decimal(amount) * self.precision)
        multiply_factor_sc = int(Decimal(multiply_factor) * self.precision)
        lifespan_sc = int(lifespan)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._insert_buy_market_order(
            base_token,
            secondary_token,
            amount_sc,
            multiply_factor_sc,
            lifespan_sc,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def _cancel_sell_order(self,
                           base_token,
                           secondary_token,
                           order_id,
                           previous_order_id,
                           **tx_arguments):
        """ cancels the sell _orderId order.
    the contract must not be paused; the caller should be the order owner """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.cancelSellOrder(
            base_token,
            secondary_token,
            order_id,
            previous_order_id,
            tx_args)

        return tx_receipt

    def cancel_sell_order(self,
                          base_token,
                          secondary_token,
                          order_id,
                          previous_order_id,
                          **tx_arguments):
        """  cancels the sell _orderId order.
    the contract must not be paused; the caller should be the order owner """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._cancel_sell_order(
            base_token,
            secondary_token,
            order_id,
            previous_order_id,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def _cancel_buy_order(self,
                          base_token,
                          secondary_token,
                          order_id,
                          previous_order_id,
                          **tx_arguments):
        """ cancels the buy _orderId order.
    the contract must not be paused; the caller should be the order owner """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.cancelBuyOrder(
            base_token,
            secondary_token,
            order_id,
            previous_order_id,
            tx_args)

        return tx_receipt

    def cancel_buy_order(self,
                         base_token,
                         secondary_token,
                         order_id,
                         previous_order_id,
                         **tx_arguments):
        """  cancels the buy _orderId order.
    the contract must not be paused; the caller should be the order owner """

        base_token = Web3.toChecksumAddress(base_token)
        secondary_token = Web3.toChecksumAddress(secondary_token)

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_receipt = self._cancel_buy_order(
            base_token,
            secondary_token,
            order_id,
            previous_order_id,
            **tx_arguments)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt

    def withdraw_commissions(self,
                             token,
                             **tx_arguments):
        """
        Withdraws all the already charged(because of a matching, a cancellation or an expiration)
        commissions of a given token
        token Address of the token to withdraw the commissions from
        """

        tx_args = self.tx_arguments(**tx_arguments)

        tx_receipt = self.sc.withdrawCommissions(
            Web3.toChecksumAddress(token),
            tx_args)

        tx_receipt.info()
        receipt_to_log(tx_receipt, self.log)

        return tx_receipt


