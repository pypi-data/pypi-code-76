"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

from web3 import Web3

from moneyonchain.events import BaseEvent


class MoCExchangeRiskProMint(BaseEvent):

    name = "RiskProMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'reserveTotal', 'commission', 'reservePrice',
                   'mocCommissionValue', 'mocPrice', 'btcMarkup', 'mocMarkup', 'vendorAccount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCExchangeRiskProWithDiscountMint(BaseEvent):
    name = "RiskProWithDiscountMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'riskProTecPrice', 'riskProDiscountPrice', 'amount',
                   'mocCommissionValue', 'mocPrice', 'btcMarkup', 'mocMarkup', 'vendorAccount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['riskProTecPrice'] = Web3.fromWei(self.event['riskProTecPrice'], 'ether')
        d_event['riskProDiscountPrice'] = Web3.fromWei(self.event['riskProDiscountPrice'], 'ether')
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['riskProTecPrice']), '.18f'),
                format(float(d_event['riskProDiscountPrice']), '.18f'),
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCExchangeStableTokenMint(BaseEvent):
    name = "StableTokenMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice',
                   'mocCommissionValue', 'mocPrice', 'btcMarkup', 'mocMarkup', 'vendorAccount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCExchangeStableTokenRedeem(BaseEvent):
    name = "StableTokenRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice',
                   'mocCommissionValue', 'mocPrice', 'btcMarkup', 'mocMarkup', 'vendorAccount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCExchangeFreeStableTokenRedeem(BaseEvent):
    name = "FreeStableTokenRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'ReserveTotal', 'Commission', 'Interests',
                   'ReservePrice', 'MoCCommission', 'MoCPrice', 'BtcMarkup', 'MoCMarkup', 'VendorAccount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeRiskProxMint(BaseEvent):
    name = "RiskProxMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',
                   'Commission',  'Reserve Price', 'MoC Commission', 'MoC Price', 'Btc Markup', 'MoC Markup', 'Vendor Account']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['bucket'] = self.event['bucket']
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['leverage'] = Web3.fromWei(self.event['leverage'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['bucket'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['leverage']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCExchangeRiskProxRedeem(BaseEvent):
    name = "RiskProxRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',
                   'Commission',  'Reserve Price', 'MoC Commission', 'MoC Price', 'Btc Markup', 'MoC Markup',
                   'Vendor Account']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['bucket'] = self.event['bucket']
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['leverage'] = Web3.fromWei(self.event['leverage'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['mocCommissionValue'] = Web3.fromWei(self.event['mocCommissionValue'], 'ether')
        d_event['mocPrice'] = Web3.fromWei(self.event['mocPrice'], 'ether')
        d_event['btcMarkup'] = Web3.fromWei(self.event['btcMarkup'], 'ether')
        d_event['mocMarkup'] = Web3.fromWei(self.event['mocMarkup'], 'ether')
        d_event['vendorAccount'] = self.event['vendorAccount']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['bucket'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['leverage']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                format(float(d_event['mocCommissionValue']), '.18f'),
                format(float(d_event['mocPrice']), '.18f'),
                format(float(d_event['btcMarkup']), '.18f'),
                format(float(d_event['mocMarkup']), '.18f'),
                d_event['vendorAccount']
                ]


class MoCStateBtcPriceProviderUpdated(BaseEvent):
    name = "BtcPriceProviderUpdated"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'oldAddress', 'newAddress']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['oldAddress'] = self.event['oldAddress']
        d_event['newAddress'] = self.event['newAddress']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['oldAddress'],
                d_event['newAddress']
                ]


class MoCStateMoCPriceProviderUpdated(BaseEvent):
    name = "MoCPriceProviderUpdated"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'oldAddress', 'newAddress']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['oldAddress'] = self.event['oldAddress']
        d_event['newAddress'] = self.event['newAddress']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['oldAddress'],
                d_event['newAddress']
                ]


class MoCStateMoCTokenChanged(BaseEvent):
    name = "MoCTokenChanged"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'mocTokenAddress']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['mocTokenAddress'] = self.event['mocTokenAddress']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['mocTokenAddress']
                ]


class MoCStateMoCVendorsChanged(BaseEvent):
    name = "MoCVendorsChanged"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'mocVendorsAddress']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['mocVendorsAddress'] = self.event['mocVendorsAddress']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['mocVendorsAddress']
                ]


class MoCVendorsVendorRegistered(BaseEvent):
    name = "VendorRegistered"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account', 'markup']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['markup'] = Web3.fromWei(self.event['markup'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['markup']), '.18f')
                ]


class MoCVendorsVendorUpdated(BaseEvent):
    name = "VendorUpdated"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account', 'markup']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['markup'] = Web3.fromWei(self.event['markup'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['markup']), '.18f')
                ]


class MoCVendorsVendorUnregistered(BaseEvent):
    name = "VendorUnregistered"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account']
                ]


class MoCVendorsVendorStakeAdded(BaseEvent):
    name = "VendorStakeAdded"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account', 'staking']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['staking'] = Web3.fromWei(self.event['staking'], 'staking')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['staking']), '.18f')
                ]


class MoCVendorsVendorStakeRemoved(BaseEvent):
    name = "VendorStakeRemoved"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account', 'staking']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['staking'] = Web3.fromWei(self.event['staking'], 'staking')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['staking']), '.18f')
                ]


class MoCVendorsTotalPaidInMoCReset(BaseEvent):
    name = "TotalPaidInMoCReset"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'account']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account']
                ]


class MoCContractLiquidated(BaseEvent):
    name = "ContractLiquidated"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'address']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['address'] = self.event['address']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['address']
                ]