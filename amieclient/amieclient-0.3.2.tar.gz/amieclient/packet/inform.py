from .base import Packet


class InformTransactionComplete(Packet):
    _packet_type = 'inform_transaction_complete'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['DetailCode', 'Message', 'StatusCode']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = []
