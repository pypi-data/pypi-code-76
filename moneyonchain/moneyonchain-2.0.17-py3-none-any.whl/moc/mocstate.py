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
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.governance import ProxyAdmin
from moneyonchain.transaction import receipt_to_log


class MoCState(ContractBase):
    contract_name = 'MoCState'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCState']

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

    def bucket_x2(self):

        result = self.sc.BUCKET_X2()

        return result

    def bucket_c0(self):

        result = self.sc.BUCKET_C0()

        return result

    def state(self, block_identifier: BlockIdentifier = 'latest'):
        """State of contract"""

        result = self.sc.state(block_identifier=block_identifier)

        return result

    def day_block_span(self, block_identifier: BlockIdentifier = 'latest'):
        """State of contract"""

        result = self.sc.dayBlockSpan(block_identifier=block_identifier)

        return result

    def smoothing_factor(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """Smoothing factor"""

        result = self.sc.getSmoothingFactor(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def rbtc_in_system(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """RBTC in system"""

        if self.mode == 'MoC':
            result = self.sc.rbtcInSystem(block_identifier=block_identifier)
        else:
            result = self.sc.reserves(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def liq(self, formatted: bool = True,
            block_identifier: BlockIdentifier = 'latest'):
        """liq"""

        result = self.sc.liq(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def cobj(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """cobj"""

        result = self.sc.cobj(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def cobj_X2(self, formatted: bool = True,
                block_identifier: BlockIdentifier = 'latest'):
        """cobj_X2"""

        result = self.sc.getBucketCobj(self.bucket_x2(), block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_mint_bpro_available(self, formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.maxMintBProAvalaible(block_identifier=block_identifier)
        else:
            result = self.sc.maxMintRiskProAvalaible(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_mint_bpro(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo"""

        if self.mode == 'MoC':
            result = self.sc.getMaxMintBPro(block_identifier=block_identifier)
        else:
            result = self.sc.getMaxMintRiskPro(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def absolute_max_doc(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == "MoC":
            result = self.sc.absoluteMaxDoc(block_identifier=block_identifier)
        else:
            result = self.sc.absoluteMaxStableToken(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bprox(self, bucket,
                  formatted: bool = True,
                  block_identifier: BlockIdentifier = 'latest'):
        """Max BProX"""

        if self.mode == 'MoC':
            result = self.sc.maxBProx(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.maxRiskProx(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bprox_btc_value(self,
                            formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        result = self.sc.maxBProxBtcValue(self.bucket_x2(), block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def absolute_max_bpro(self, formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.absoluteMaxBPro(block_identifier=block_identifier)
        else:
            result = self.sc.absoluteMaxRiskPro(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def free_doc(self, formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.freeDoc(block_identifier=block_identifier)
        else:
            result = self.sc.freeStableToken(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def leverage(self, bucket,
                 formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """Leverage"""

        result = self.sc.leverage(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_discount_rate(self,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """BPro discount rate"""

        if self.mode == 'MoC':
            result = self.sc.bproSpotDiscountRate(block_identifier=block_identifier)
        else:
            result = self.sc.riskProSpotDiscountRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bpro_with_discount(self,
                               formatted: bool = True,
                               block_identifier: BlockIdentifier = 'latest'):
        """Max BPro with discount"""

        if self.mode == 'MoC':
            result = self.sc.maxBProWithDiscount(block_identifier=block_identifier)
        else:
            result = self.sc.maxRiskProWithDiscount(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_discount_price(self,
                            formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """BPro discount price"""

        if self.mode == 'MoC':
            result = self.sc.bproDiscountPrice(block_identifier=block_identifier)
        else:
            result = self.sc.riskProDiscountPrice(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def blocks_to_settlement(self, block_identifier: BlockIdentifier = 'latest'):
        """Blocks to settlement"""

        result = self.sc.blocksToSettlement(block_identifier=block_identifier)

        return result

    def bitcoin_price(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin price in USD.
        NOTE: This call have a required if the price is valid, so it can fail.
        """

        if self.mode == 'MoC':
            result = self.sc.getBitcoinPrice(block_identifier=block_identifier)
        else:
            result = self.sc.getReserveTokenPrice(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_price(self, formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """BPro price in USD"""

        if self.mode == 'MoC':
            result = self.sc.bproUsdPrice(block_identifier=block_identifier)
        else:
            result = self.sc.riskProUsdPrice(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_tec_price(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """BPro Technical price in RBTC"""

        if self.mode == 'MoC':
            result = self.sc.bproTecPrice(block_identifier=block_identifier)
        else:
            result = self.sc.riskProTecPrice(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bprox_price(self,
                    bucket=None,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """BProX price in RBTC"""

        if not bucket:
            bucket = self.bucket_x2()

        if self.mode == "MoC":
            result = self.sc.bproxBProPrice(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.riskProxRiskProPrice(bucket, block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def btc2x_tec_price(self,
                        bucket=None,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """BTC2X Technical price in RBTC"""

        if not bucket:
            bucket = self.bucket_x2()

        if self.mode == 'MoC':
            result = self.sc.bucketBProTecPrice(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.bucketRiskProTecPrice(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitcoin_moving_average(self, formatted: bool = True,
                               block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin Moving Average price in USD"""

        if self.mode == 'MoC':
            result = self.sc.getBitcoinMovingAverage(block_identifier=block_identifier)
        else:
            result = self.sc.getExponentalMovingAverage(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def global_locked_reserve_tokens(self,
                                     formatted: bool = True,
                                     block_identifier: BlockIdentifier = 'latest'):
        """ lockedReserveTokens amount """

        if self.mode == 'MoC':
            result = self.sc.globalLockedBitcoin(block_identifier=block_identifier)
        else:
            result = self.sc.globalLockedReserveTokens(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def reserves_remainder(self,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """ Reserves remainder """

        if self.mode == 'MoC':
            result = self.sc.getRbtcRemainder(block_identifier=block_identifier)
        else:
            result = self.sc.getReservesRemainder(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def get_inrate_bag(self, bucket,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """Get inrate Bag"""

        result = self.sc.getInrateBag(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_nbtc(self, bucket,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Bucket NBTC"""

        if self.mode == "MoC":
            result = self.sc.getBucketNBTC(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.getBucketNReserve(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_ndoc(self, bucket,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Bucket NDOC"""

        if self.mode == "MoC":
            result = self.sc.getBucketNDoc(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.getBucketNStableToken(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_nbpro(self, bucket,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """Bucket NBPRO"""

        if self.mode == "MoC":
            result = self.sc.getBucketNBPro(bucket, block_identifier=block_identifier)
        else:
            result = self.sc.getBucketNRiskPro(bucket, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def days_to_settlement(self, formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """Days to settlement"""

        result = int(self.sc.daysToSettlement(block_identifier=block_identifier))

        return result

    def coverage(self, bucket,
                 formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """coverage"""

        result = self.sc.coverage(bucket, block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def global_coverage(self, formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """Global coverage"""

        result = self.sc.globalCoverage(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitpro_total_supply(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """Bitpro total supply"""

        if self.mode == 'MoC':
            result = self.sc.bproTotalSupply(block_identifier=block_identifier)
        else:
            result = self.sc.riskProTotalSupply(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_total_supply(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """DOC total supply"""

        if self.mode == 'MoC':
            result = self.sc.docTotalSupply(block_identifier=block_identifier)
        else:
            result = self.sc.stableTokenTotalSupply(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def is_liquidation(self, block_identifier: BlockIdentifier = 'latest'):
        """DOC total supply"""

        result = self.sc.isLiquidationReached(block_identifier=block_identifier)

        return result

    def is_calculate_ema(self, block_identifier: BlockIdentifier = 'latest'):
        """Is time to calculate ema"""

        result = self.sc.shouldCalculateEma(block_identifier=block_identifier)

        return result

    def price_provider(self, block_identifier: BlockIdentifier = 'latest'):
        """Price provider address"""

        if self.mode == 'MoC':
            result = self.sc.getBtcPriceProvider(block_identifier=block_identifier)
        else:
            result = self.sc.getPriceProvider(block_identifier=block_identifier)

        return result

    def liquidation_price(self,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Liquidation price """

        result = self.sc.getLiquidationPrice(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def current_abundance_ratio(self,
                                formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """ relation between stableTokens in bucket 0 and StableToken total supply """

        result = self.sc.currentAbundanceRatio(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def abundance_ratio(self,
                        amount,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """ Abundance ratio, receives tha amount of stableToken to use the value of
        stableToken0 and StableToken total supply """

        result = self.sc.abundanceRatio(amount, block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def execute_calculate_ema(self,
                              **tx_arguments):
        """Execute calculate ema """

        tx_receipt = None
        if self.is_calculate_ema():

            self.log.info("Calling calculateBitcoinMovingAverage ...")

            tx_args = self.tx_arguments(**tx_arguments)

            if self.mode == 'MoC':
                tx_receipt = self.sc.calculateBitcoinMovingAverage(tx_args)
            else:
                tx_receipt = self.sc.calculateReserveTokenMovingAverage(tx_args)

            tx_receipt.info()
            receipt_to_log(tx_receipt, self.log)

        return tx_receipt
