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

from .utils import array_to_dictionary


class VENDORSMoCVendors(ContractBase):
    contract_name = 'MoCVendors'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCVendors.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCVendors.bin'))

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
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCVendors']

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

    def get_vendor(self,
                   vendor_account,
                   formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """Gets vendor from mapping"""

        vendor_details = self.sc.vendors(vendor_account, block_identifier=block_identifier)

        print(vendor_details)

        names_array = ["isActive", "markup", "totalPaidInMoC", "staking", "paidMoC", "paidRBTC"]

        if formatted:
            vendor_details = [Web3.fromWei(unformatted_value, 'ether') for unformatted_value in vendor_details[1:]]

        return array_to_dictionary(vendor_details, names_array)

    def get_vendors_addresses(self,
                              block_identifier: BlockIdentifier = 'latest'):
        """Gets all active vendors addresses"""

        vendor_count = self.sc.getVendorsCount(block_identifier=block_identifier)
        result = []

        for i in range(0, vendor_count):
            result.append(self.sc.vendorsList(i, block_identifier=block_identifier))

        return result

    def get_vendors(self,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Gets all active vendors from mapping"""

        vendors_list = self.get_vendors_addresses()

        result = {}

        for vendor in vendors_list:
            result[vendor] = self.get_vendor(vendor)

        return result
