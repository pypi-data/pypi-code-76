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

from web3 import Web3


from moneyonchain.contract import ContractBase


class TokenPriceProviderLastClosingPrice(ContractBase):

    contract_name = 'TokenPriceProviderLastClosingPrice'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPriceProviderLastClosingPrice.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/TokenPriceProviderLastClosingPrice.bin'))

    mode = 'DEX'

    def constructor(self, base_token, secondary_token, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class MocBproBtcPriceProviderFallback(ContractBase):

    contract_name = 'MocBproBtcPriceProviderFallback'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocBproBtcPriceProviderFallback.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocBproBtcPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token, **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(moc_state),
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class MocBproUsdPriceProviderFallback(ContractBase):
    log = logging.getLogger()

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocBproUsdPriceProviderFallback.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocBproUsdPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token, **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(moc_state),
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class UnityPriceProvider(ContractBase):
    contract_name = 'UnityPriceProvider'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/UnityPriceProvider.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/UnityPriceProvider.bin'))

    mode = 'DEX'

    def constructor(self, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(**tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class ExternalOraclePriceProviderFallback(ContractBase):
    contract_name = 'ExternalOraclePriceProviderFallback'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ExternalOraclePriceProviderFallback.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ExternalOraclePriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, external_price_provider, base_token, secondary_token, **tx_arguments):
        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(external_price_provider),
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class MocRiskProReservePriceProviderFallback(ContractBase):

    contract_name = 'MocRiskProReservePriceProviderFallback'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocRiskProReservePriceProviderFallback.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocRiskProReservePriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(moc_state),
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt


class MocRiskProUsdPriceProviderFallback(ContractBase):

    contract_name = 'MocRiskProUsdPriceProviderFallback'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocRiskProUsdPriceProviderFallback.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocRiskProUsdPriceProviderFallback.bin'))

    mode = 'DEX'

    def constructor(self, moc_state, base_token, secondary_token, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = Web3.toChecksumAddress(
            self.network_manager.options['networks'][config_network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(moc_state),
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(base_token),
            Web3.toChecksumAddress(secondary_token),
            **tx_arguments
            )

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Contract Address: {address}".format(address=tx_receipt.contract_address))

        return tx_receipt
