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


BUCKET_X2 = '0x5832000000000000000000000000000000000000000000000000000000000000'
BUCKET_C0 = '0x4330000000000000000000000000000000000000000000000000000000000000'


class MoCInrate(ContractBase):
    contract_name = 'MoCInrate'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCInrate']

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

    def commision_rate(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """Gets commision rate"""

        result = self.sc.getCommissionRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitpro_rate(self, formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Gets the rate for BitPro/RiskProHolder Holders"""

        if self.mode == 'MoC':
            result = self.sc.getBitProRate(block_identifier=block_identifier)
        else:
            result = self.sc.getRiskProRate(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitpro_interest_blockspan(self,
                                  block_identifier: BlockIdentifier = 'latest'):
        """Gets the blockspan of BPRO that represents the frecuency of BitPro holders intereset payment"""

        if self.mode == 'MoC':
            result = self.sc.getBitProInterestBlockSpan(block_identifier=block_identifier)
        else:
            result = self.sc.getRiskProInterestBlockSpan(block_identifier=block_identifier)

        return result

    def last_bitpro_interest_block(self,
                                   block_identifier: BlockIdentifier = 'latest'):
        """ Last block when an BitPro holders instereste was calculated"""

        if self.mode == 'MoC':
            result = self.sc.lastBitProInterestBlock(block_identifier=block_identifier)
        else:
            result = self.sc.lastRiskProInterestBlock(block_identifier=block_identifier)

        return result

    def daily_enabled(self,
                      formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.isDailyEnabled(block_identifier=block_identifier)

        return result

    def daily_inrate(self, formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """returns the amount of BTC to pay in concept of interest"""

        result = self.sc.dailyInrate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def spot_inrate(self, formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.spotInrate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def commission_rate(self,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.getCommissionRate(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def commission_address(self, block_identifier: BlockIdentifier = 'latest'):
        """Returns the address of the target receiver of commissions"""

        result = self.sc.commissionsAddress(block_identifier=block_identifier)

        return result

    def last_daily_pay(self,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """returns the amount of BTC to pay in concept of interest"""

        result = self.sc.lastDailyPayBlock(block_identifier=block_identifier)

        return result

    def calc_commission_value(self,
                              amount,
                              formatted: bool = True,
                              block_identifier: BlockIdentifier = 'latest'):
        """ Calc commission value amount in ether float"""

        result = self.sc.calcCommissionValue(int(amount * self.precision),
                                             block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def calc_mint_interest_value(self, amount,
                                 formatted: bool = True,
                                 precision: bool = True,
                                 block_identifier: BlockIdentifier = 'latest'):
        """ Calc interest value amount in ether float"""

        bucket = BUCKET_X2

        if precision:
            amount = int(amount * self.precision)
        result = self.sc.calcMintInterestValues(bucket, int(amount),
                                                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def calc_bitpro_holders_interest(self, formatted: bool = True,
                                     block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.calculateBitProHoldersInterest(block_identifier=block_identifier)
        else:
            result = self.sc.calculateRiskProHoldersInterest(block_identifier=block_identifier)

        if formatted:
            result = [Web3.fromWei(result[0], 'ether'), Web3.fromWei(result[1], 'ether')]

        return result

    def bitpro_interest_address(self, formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.getBitProInterestAddress(block_identifier=block_identifier)
        else:
            result = self.sc.getRiskProInterestAddress(block_identifier=block_identifier)

        return result

    def is_bitpro_interest_enabled(self, formatted: bool = True,
                                   block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.isBitProInterestEnabled(block_identifier=block_identifier)
        else:
            result = self.sc.isRiskProInterestEnabled(block_identifier=block_identifier)

        return result

    def doc_inrate_avg(self,
                       amount,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """ Calculates an average interest rate between after and before free doc Redemption"""

        if self.mode == 'MoC':
            result = self.sc.docInrateAvg(int(amount * self.precision), block_identifier=block_identifier)
        else:
            result = self.sc.stableTokenInrateAvg(int(amount * self.precision),
                                                  block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def btc2x_inrate_avg(self, amount, on_minting=False, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """ Calculates an average interest rate between after and before mint/redeem """

        bucket = BUCKET_X2

        if self.mode == 'MoC':
            result = self.sc.btcxInrateAvg(bucket, int(amount * self.precision), on_minting,
                                           block_identifier=block_identifier)
        else:
            result = self.sc.riskProxInrateAvg(bucket, int(amount * self.precision), on_minting,
                                               block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_inrate(self,
                   formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate Doc"""

        info = dict()

        result = self.sc.getDoCTmax(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['DoCTmax'] = result

        result = self.sc.getDoCPower(block_identifier=block_identifier)
        info['DoCPower'] = result

        result = self.sc.getDoCTmin(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['DoCTmin'] = result

        return info

    def btcx_inrate(self,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate btcx"""

        info = dict()

        result = self.sc.getBtcxTmax(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['BtcxTmax'] = result

        result = self.sc.getBtcxPower(block_identifier=block_identifier)
        info['BtcxPower'] = result

        result = self.sc.getBtcxTmin(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['BtcxTmin'] = result

        return info
