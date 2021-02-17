import pytest

from ..packet import (Packet, RequestAccountCreate, Packet, PacketInvalidData,
                      NotifyAccountCreate, NotifyPersonDuplicate,
                      NotifyUserModify, RequestUserModify)
from .fixtures import DEMO_JSON_PKT_1, DEMO_JSON_PKT_2


class TestClient:
    """
    Test packet creation and processing.
    """

    def test_creation(self):
        """
        Test that we create a packet of the proper kind
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        assert packet.packet_type == 'request_account_create'
        assert isinstance(packet, RequestAccountCreate)

    def test_additional_data(self):
        """
        Test that additional data is stored properly
        DEMO_JSON_PKT_1 contains a parameter that is
        not part of the current AMIE spec, UserFavoriteColor,
        so we check for that
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        assert 'UserFavoriteColor' in packet.additional_data
        assert packet.additional_data['UserFavoriteColor'] == 'blue'

    def test_required_data_storage(self):
        """
        Required data is stored in the proper location on a created packet
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        for k in RequestAccountCreate._data_keys_required:
            assert k in packet._required_data
            assert getattr(packet, k) == DEMO_JSON_PKT_1['body'].get(k)
            assert packet._required_data.get(k) == DEMO_JSON_PKT_1['body'].get(k)

    def test_required_data_delete_is_none(self):
        """
        If we 'del' a field of required data from the packet,
        it's replaced with None, not removed from the object
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        for k in RequestAccountCreate._data_keys_required:
            delattr(packet, k)
            assert getattr(packet, k) is None
            assert packet._required_data[k] is None

    def test_allowed_data_storage(self):
        """
        Parameters that are defined in the AMIE spec but optional are stored
        in the right location.
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        for k in RequestAccountCreate._data_keys_allowed:
            if k in packet._allowed_data:
                assert getattr(packet, k) == DEMO_JSON_PKT_1['body'].get(k)
                assert packet._allowed_data.get(k) == DEMO_JSON_PKT_1['body'].get(k)

    def test_reply_packet_validation(self):
        """
        The in_reply_to field and the packet type are properly set on a packet
        generated via the reply_packet method. Additionally, that packet passes
        validation check even if required data is missing.
        """
        parent_packet = Packet.from_dict(DEMO_JSON_PKT_1)
        reply_packet = parent_packet.reply_packet()
        assert reply_packet.in_reply_to_id == parent_packet.packet_rec_id
        assert reply_packet.packet_type == 'notify_account_create'
        assert isinstance(reply_packet, NotifyAccountCreate)
        for k in NotifyAccountCreate._data_keys_not_required_in_reply:
            v = getattr(reply_packet, k)
            delattr(reply_packet, k)
            assert reply_packet.validate_data()
            # Replace the data so we're not double-testing
            setattr(reply_packet, k, v)

    def test_reply_packet_missing(self):
        """
        The in_reply_to field and the packet type are properly set on a packet
        generated via the reply_packet method. Additionally, that packet passes
        validation check even if required data is missing.
        """
        parent_packet = Packet.from_dict(DEMO_JSON_PKT_1)
        reply_packet = parent_packet.reply_packet()
        assert reply_packet.in_reply_to_id == parent_packet.packet_rec_id
        assert reply_packet.packet_type == 'notify_account_create'
        assert isinstance(reply_packet, NotifyAccountCreate)
        actually_required_keys = list(set(NotifyAccountCreate._data_keys_required) -
                                      set(NotifyAccountCreate._data_keys_not_required_in_reply))
        for k in actually_required_keys:
            v = getattr(reply_packet, k)
            delattr(reply_packet, k)
            assert k in reply_packet.missing_attributes()
            # Replace the data so we're not double-testing
            setattr(reply_packet, k, v)


    def test_validation_required_data(self):
        """
        Packet validation in the general case fails if required data is missing
        """
        packet = Packet.from_dict(DEMO_JSON_PKT_1)
        for k in RequestAccountCreate._data_keys_required:
            v = getattr(packet, k)
            delattr(packet, k)
            with pytest.raises(PacketInvalidData):
                packet.validate_data(raise_on_invalid=True)
            assert not packet.validate_data()
            # Replace the data so we're not double-testing
            setattr(packet, k, v)

    def test_validation_notify_person_duplicate(self):
        """
        Packet validation for NotifyPersonDuplicate packets
        """
        npd_packet = NotifyPersonDuplicate('12345',
                                           PersonID1='abcde',
                                           PersonID2='abcde',
                                           GlobalID1='abcde',
                                           GlobalID2='abcde'
                                           )

        # Test when everything is provided
        assert npd_packet.validate_data()

        err_regex = r'Must provide either GlobalID[12] or PersonID[12]'
        for pid, gid in [('PersonID1', 'GlobalID1'),
                         ('PersonID2', 'GlobalID2')]:
            # Test when both PID and GID are not provided
            setattr(npd_packet, pid, None)
            setattr(npd_packet, gid, None)
            with pytest.raises(PacketInvalidData, match=err_regex):
                npd_packet.validate_data(raise_on_invalid=True)
            assert not npd_packet.validate_data()

            # Test when only PID is provided
            setattr(npd_packet, pid, 'abcde')
            assert npd_packet.validate_data()
            # Test when only GID is provided
            setattr(npd_packet, gid, 'abcde')
            setattr(npd_packet, pid, None)
            assert npd_packet.validate_data()

    def test_validation_notify_user_modify(self):
        """
        Packet validation for NotifyUserModify packets
        """
        num_packet = NotifyUserModify('12345', PersonID='abcde')
        # test missing action type
        with pytest.raises(PacketInvalidData):
            num_packet.validate_data(raise_on_invalid=True)
        assert not num_packet.validate_data()

        # Test valid action types
        for action_type in ['add', 'delete', 'replace']:
            num_packet.ActionType = action_type
            assert num_packet.validate_data()

        # Test invalid action type
        num_packet.ActionType = 'make_just_a_little_bit_taller'
        with pytest.raises(PacketInvalidData):
            num_packet.validate_data(raise_on_invalid=True)
        assert not num_packet.validate_data()

    def test_validation_request_user_modify(self):
        """
        Packet validation for RequestUserModify packets
        """
        rum_packet = RequestUserModify('12345', PersonID='abcde')
        # test missing action type
        with pytest.raises(PacketInvalidData):
            rum_packet.validate_data(raise_on_invalid=True)
        assert not rum_packet.validate_data()

        # Test valid action types
        for action_type in ['add', 'delete', 'replace']:
            rum_packet.ActionType = action_type
            assert rum_packet.validate_data()

        # Test invalid action type
        rum_packet.ActionType = 'make_just_a_little_bit_taller'
        with pytest.raises(PacketInvalidData):
            rum_packet.validate_data(raise_on_invalid=True)
        assert not rum_packet.validate_data()

    def test_packet_fidelity(self):
        """
        Make sure that the data we put into the packet is the same as the data
        we get out, especially if we have two packets of the same type.
        See https://github.com/XSEDE/amieclient/issues/8 &
        https://github.com/XSEDE/amieclient/commit/7c57ce781b70e5a06a1b3811d1f11d9f99a20893
        for why we check both packets here
        """
        packet_1 = Packet.from_dict(DEMO_JSON_PKT_1)
        packet_2 = Packet.from_dict(DEMO_JSON_PKT_2)

        # Check that the _original_data field matches
        assert packet_1._original_data == DEMO_JSON_PKT_1
        assert packet_2._original_data == DEMO_JSON_PKT_2

        # Check that we process the data properly
        for pkt in [packet_1, packet_2]:
            for k, v in pkt._original_data['header'].items():
                # skip header fields we handle elsewhere
                if k in ['expected_reply_list']:
                    continue
                assert getattr(pkt, k) == v
            for k, v in pkt._original_data['body'].items():
                try:
                    pkt_v = getattr(pkt, k)
                except AttributeError:
                    # Handle additional data that's kept separate
                    pkt_v = pkt.additional_data[k]
                assert pkt_v == v
