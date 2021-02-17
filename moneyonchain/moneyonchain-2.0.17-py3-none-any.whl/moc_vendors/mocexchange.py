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
from moneyonchain.moc import MoCExchange

from .utils import array_to_dictionary


class VENDORSMoCExchange(MoCExchange):
    contract_name = 'MoCExchange'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCExchange.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCExchange.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def calculate_commissions_with_prices(self,
                                          amount,
                                          tx_type_fees_MOC,
                                          tx_type_fees_RBTC,
                                          vendor_account,
                                          default_account=None,
                                          formatted: bool = True):
        """ Calc commission value and vendor markup amount in ether float """

        if not default_account:
            default_account = 0

        params = [self.network_manager.accounts[default_account].address,
                  int(amount * self.precision),
                  tx_type_fees_MOC,
                  tx_type_fees_RBTC,
                  vendor_account]

        names_array = ["btcCommission", "mocCommission", "btcPrice", "mocPrice", "btcMarkup", "mocMarkup"]

        if self.mode == 'MoC':
            result = self.sc.calculateCommissionsWithPrices(params)
        else:
            raise NotImplementedError('Only supported in MoC mode')

        if formatted:
            result = [Web3.fromWei(unformatted_value, 'ether') for unformatted_value in result]

        return array_to_dictionary(result, names_array)

    def moc_token_balance(self,
                          owner_address,
                          spender_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):

        owner_address = Web3.toChecksumAddress(owner_address)
        spender_address = Web3.toChecksumAddress(spender_address)

        result = self.sc.getMoCTokenBalance(
            owner_address,
            spender_address,
            block_identifier=block_identifier)

        if formatted:
            result = (Web3.fromWei(result[0], 'ether'), Web3.fromWei(result[0], 'ether'))

        return result

