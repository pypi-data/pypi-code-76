"""
AMIE packets relating to persons
"""

from .base import Packet, PacketInvalidData


class NotifyPersonDuplicate(Packet):
    _packet_type = 'notify_person_duplicate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = []
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['GlobalID1', 'GlobalID2', 'PersonID1', 'PersonID2']

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there are no unallowed tags, and additionally checks to
        make sure that either a global ID or person ID is provided for
        the two duplicate people
        """
        if (self._allowed_data.get('GlobalID1') is None and
                self._allowed_data.get('PersonID1') is None):
            if raise_on_invalid:
                raise PacketInvalidData('Must provide either GlobalID1 or PersonID1')
            else:
                return False
        if (self._allowed_data.get('GlobalID2') is None and
                self._allowed_data.get('PersonID2') is None):
            if raise_on_invalid:
                raise PacketInvalidData('Must provide either GlobalID2 or PersonID2')
            else:
                return False
        return super().validate_data(raise_on_invalid)


class NotifyPersonIDs(Packet):
    _packet_type = 'notify_person_ids'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'PrimaryPersonID']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['PersonIDList', 'RemoveResourceList', 'ResourceLogin']


class RequestPersonMerge(Packet):
    _packet_type = 'request_person_merge'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['KeepGlobalID', 'KeepPersonID', 'DeleteGlobalID',
                           'DeletePersonID']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['DeletePortalLogin', 'KeepPortalLogin']
