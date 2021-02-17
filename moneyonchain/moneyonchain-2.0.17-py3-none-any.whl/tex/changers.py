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
from moneyonchain.contract import ContractBase
from moneyonchain.changers import BaseChanger
from moneyonchain.governance import DEXGovernor


class DexAddTokenPairChanger(BaseChanger):

    contract_name = 'DexAddTokenPairChanger'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/AddTokenPairChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/AddTokenPairChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_address,
                    price_provider,
                    price_precision,
                    init_price,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            contract_address,
            [Web3.toChecksumAddress(base_token)],
            [Web3.toChecksumAddress(secondary_address)],
            [Web3.toChecksumAddress(price_provider)],
            [price_precision],
            [init_price],
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexMaxOrderLifespanChanger(BaseChanger):

    contract_name = 'DexMaxOrderLifespanChanger'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MaxOrderLifespanChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MaxOrderLifespanChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    order_lifespan,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            contract_address,
            order_lifespan,
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexTokenPairDisabler(BaseChanger):

    contract_name = 'DexTokenPairDisabler'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPairDisabler.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPairDisabler.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_address,
                    secondary_address,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 Web3.toChecksumAddress(base_address),
                                 Web3.toChecksumAddress(secondary_address),
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexTokenPairEnabler(BaseChanger):

    contract_name = 'DexTokenPairEnabler'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPairEnabler.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPairEnabler.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_address,
                    secondary_address,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 Web3.toChecksumAddress(base_address),
                                 Web3.toChecksumAddress(secondary_address),
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexEMAPriceChanger(BaseChanger):

    contract_name = 'DexMaxOrderLifespanChanger'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/EMAPriceChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/EMAPriceChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_token,
                    ema_price,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 Web3.toChecksumAddress(base_token),
                                 Web3.toChecksumAddress(secondary_token),
                                 ema_price,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexPriceProviderChanger(BaseChanger):

    contract_name = 'DexPriceProviderChanger'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_token,
                    price_provider,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 Web3.toChecksumAddress(base_token),
                                 Web3.toChecksumAddress(secondary_token),
                                 Web3.toChecksumAddress(price_provider),
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexMaxBlocksForTickChanger(BaseChanger):
    contract_name = 'DexMaxBlocksForTickChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MaxBlocksForTickChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MaxBlocksForTickChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    max_blocks_for_ticks,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 max_blocks_for_ticks,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexMinBlocksForTickChanger(BaseChanger):

    contract_name = 'DexMinBlocksForTickChanger'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinBlocksForTickChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinBlocksForTickChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    min_blocks_for_ticks,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 min_blocks_for_ticks,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexCommissionRateChanger(BaseChanger):

    contract_name = 'DexCommissionRateChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionRateChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionRateChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    commission_rate,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 commission_rate,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexMinOrderAmountChanger(BaseChanger):

    contract_name = 'DexMinOrderAmountChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinOrderAmountChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinOrderAmountChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    min_order_amount,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 min_order_amount,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexCancelationPenaltyRateChanger(BaseChanger):
    contract_name = 'DexCancelationPenaltyRateChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CancelationPenaltyRateChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CancelationPenaltyRateChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    cancelation_penalty_rate,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 cancelation_penalty_rate,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexExpirationPenaltyRateChanger(BaseChanger):

    contract_name = 'DexExpirationPenaltyRateChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ExpirationPenaltyRateChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ExpirationPenaltyRateChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    expiration_penalty_rate,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 expiration_penalty_rate,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class DexMinimumCommissionChanger(BaseChanger):
    contract_name = 'DexTokenPairEnabler'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinimumCommissionChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MinimumCommissionChanger.bin'))

    mode = 'DEX'

    def constructor(self,
                    minimum_commission,
                    execute_change=False,
                    **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address,
                                 minimum_commission,
                                 **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = DEXGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt
