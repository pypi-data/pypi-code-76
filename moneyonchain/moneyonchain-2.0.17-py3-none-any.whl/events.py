"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import datetime
from tabulate import tabulate


class BaseEvent(object):
    name = "BaseEvent"
    hours_delta = 0

    def __init__(self, event, tx_receipt=None):

        # if tx_receipt get info from receipt
        # if no, get from event
        if tx_receipt:
            self.blockNumber = tx_receipt.block_number
            self.transactionHash = tx_receipt.txid
            self.timestamp = datetime.datetime.fromtimestamp(tx_receipt.timestamp)
            self.event = event
        else:
            self.blockNumber = event['blockNumber']
            self.transactionHash = event['transactionHash']
            self.timestamp = event['timestamp']
            self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = []
        return columns

    def formatted(self):
        d_event = dict()

        return d_event

    def row(self):
        d_event = self.formatted()
        return []

    def print_table(self):
        return tabulate([self.row()], headers=self.columns(), tablefmt="pipe")

    def print_row(self):
        return tabulate([self.row()], tablefmt="pipe")
