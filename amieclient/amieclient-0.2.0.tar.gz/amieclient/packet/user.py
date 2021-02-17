"""
AMIE packets relating to users
"""

from .base import Packet, PacketInvalidData


class NotifyUserModify(Packet):
    _packet_type = 'notify_account_inactivate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = [
        'ActionType',
        'PersonID',
    ]
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = [
        'AcademicDegree',
        'BusinessPhoneComment',
        'BusinessPhoneExtension',
        'BusinessPhoneNumber',
        'City',
        'Country',
        'Department',
        'DnList',
        'Email',
        'Fax',
        'FirstName',
        'HomePhoneComment',
        'HomePhoneExtension',
        'HomePhoneNumber',
        'LastName',
        'MiddleName',
        'Organization',
        'OrgCode',
        'State'
    ]

    def validate_data(self, raise_on_invalid=False):
        action_type = self.ActionType
        if action_type not in ['add', 'delete', 'replace']:
            if raise_on_invalid:
                error_str = 'Invalid action type for notify_user_modify: "{}"'.format(action_type)
                raise PacketInvalidData(error_str)
            else:
                return False
        return super().validate_data(raise_on_invalid)


class RequestUserModify(Packet):
    _packet_type = 'request_user_modify'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = [
        'ActionType',
        'PersonID',
    ]
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = [
        'AcademicDegree',
        'BusinessPhoneComment',
        'BusinessPhoneExtension',
        'BusinessPhoneNumber',
        'CitizenshipList',
        'CitizenshipList',
        'City',
        'Country',
        'Department',
        'DnList',
        'Email',
        'Fax',
        'FirstName',
        'HomePhoneComment',
        'HomePhoneExtension',
        'HomePhoneNumber',
        'LastName',
        'MiddleName',
        'NsfStatusCode',
        'Organization',
        'OrgCode',
        'State',
        'StreetAddress',
        'StreetAddress2',
        'Title',
        'Zip',
    ]

    def validate_data(self, raise_on_invalid=False):
        action_type = self.ActionType
        if action_type not in ['add', 'delete', 'replace']:
            if raise_on_invalid:
                error_str = 'Invalid action type for request_user_modify: "{}"'.format(action_type)
                raise PacketInvalidData(error_str)
            else:
                return False
        return super().validate_data(raise_on_invalid)
