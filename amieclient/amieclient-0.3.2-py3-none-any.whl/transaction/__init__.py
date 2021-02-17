import json
from datetime import datetime

from ..packet.base import Packet


class Transaction(object):
    def __init__(self, transaction_id, state,
                 originating_site, local_site, remote_site,
                 packets=None):
        self.id = transaction_id
        self.state = state
        self.originating_site = originating_site
        self.local_site = local_site
        self.remote_site = remote_site
        if packets:
            self.packets = packets
        else:
            self.packets = []

    @classmethod
    def from_dict(cls, dict_in):
        tx = cls(
                 transaction_id=dict_in['transaction_id'],
                 state=dict_in['state'],
                 originating_site=dict_in['originating_site_name'],
                 local_site=dict_in['local_site_name'],
                 remote_site=dict_in['remote_site_name'],
                 packets=[Packet.from_dict(p) for p in dict_in['DATA']]
        )
        return tx

    @classmethod
    def from_json(cls, json_in):
        tx_in = json.loads(json_in)
        return cls.from_dict(tx_in)

    def as_dict(self):
        data_dict = {
            'DATA_TYPE': 'transaction',
            'transaction_ID': self.id,
            'originating_site_name':  self.originating_site,
            'local_site_name': self.local_site,
            'remote_site_name': self.remote_site,
            'state': self.state,
            'DATA': [pkt.as_dict() for pkt in self.packets]
        }

        return data_dict

    def json(self):
        data_dict = self.as_dict()
        return json.dumps(data_dict)

class TransactionList(object):
    """
    List of transactions.
    """

    def __init__(self, length, limit, offset, total, transactions=None):
        self.length = length
        self.limit = limit
        self.offset = offset
        self.total = total
        if transactions is not None:
            self.transactions = transactions
        else:
            self.transactions = []

    @classmethod
    def from_dict(cls, dict_in):
        tx_list = cls(
            length=dict_in['length'],
            limit=dict_in['limit'],
            offset=dict_in['offset'],
            total=dict_in['total'],
            transactions=[Transaction.from_dict(d) for d in dict_in['DATA']]
        )
        return tx_list

    @classmethod
    def from_json(cls, json_in):
        txlist_in = json.loads(json_in)
        return cls.from_dict(txlist_in)

    def as_dict(self):
        data_dict = {
            'DATA_TYPE': 'transaction_list',
            'length':  self.legth,
            'limit': self.limit,
            'offset': self.offset,
            'total': self.total,
            'DATA': [txn.as_dict() for txn in self.transactions]
        }
        return data_dict

    def json(self, **json_kwargs):
        """
        The JSON representation of this AMIE transaction
        """
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))
