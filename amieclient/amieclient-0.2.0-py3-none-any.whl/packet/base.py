import json

from datetime import datetime
from collections import defaultdict
from dateutil.parser import parse as dtparse


class PacketInvalidData(Exception):
    """Raised when we try to build a packet with invalid data"""
    pass


class PacketInvalidType(Exception):
    """Raised when we try to create a packet with an invalid type"""


# Closures, for properly handling properties
# in the metaclass
def _make_get_required(key):
    def get_required(self):
        return self._required_data.get(key)
    return get_required


def _make_set_required(key):
    def set_required(self, value):
        self._required_data[key] = value
    return set_required


def _make_del_required(key):
    def del_required(self):
        self._required_data[key] = None
    return del_required


def _make_get_allowed(key):
    def get_allowed(self):
        return self._allowed_data.get(key)
    return get_allowed


def _make_set_allowed(key):
    def set_allowed(self, value):
        self._allowed_data[key] = value
    return set_allowed


class MetaPacket(type):
    """Metaclass for packets.

    Looks at the _data_keys_allowed and _data_keys_required attributes
    when a subclass is declared, then adds class properties that
    stores the information in two separate dictionaries on the object.
    """
    def __new__(cls, name, base, attrs):
        required_fields = attrs.get('_data_keys_required', [])
        allowed_fields = attrs.get('_data_keys_allowed', [])
        for k in required_fields:
            attrs[k] = property(_make_get_required(k),
                                _make_set_required(k),
                                _make_del_required(k))
        for k in allowed_fields:
            attrs[k] = property(_make_get_allowed(k), _make_set_allowed(k))

        # fix expected_replies to add a default timeouts
        expected_replies = attrs.get('_expected_reply', [])
        expected_with_timeouts = []
        for r in expected_replies:
            if isinstance(r, dict):
                expected_with_timeouts.append(r)
            elif isinstance(r, Packet):
                expected_with_timeouts.append(
                    {'type': r._packet_type,
                     'timeout': 30240}
                )
            elif isinstance(r, str):
                expected_with_timeouts.append(
                    {'type': r,
                     'timeout': 30240}
                )
            else:
                raise Exception("Invalid reply_type")
        attrs['expected_reply'] = expected_with_timeouts
        return type.__new__(cls, name, base, attrs)


class Packet(object, metaclass=MetaPacket):
    """
    Generic AMIE packet base class

    Class parameters:
        _packet_type: the type of the packet (string)
        _expected_reply: expected reply types (list[string] or list[Packet type])
        _data_keys_required: Data keys that are required for this packet type
        _data_keys_not_required_in_reply: Data keys that are required but
                                          whose value can be inferred if
                                          this is a reply packet
        _data_keys_allowed: Data keys that are allowed for this packet type


    Args:
        packet_rec_id (str): The ID for this packet
        date (datetime.Datetime): A datetime object representing this packet's date attribute
        additional_data (dict): Body data that is outsite the AMIE spec.
        in_reply_to (str, int, amieclient.Packet): The packet this packet is in response to. Can take a packet, int, string, or None.
    """
    _data_keys_required = []
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = []
    _expected_replies = []

    def __init__(self, packet_rec_id=None, trans_rec_id=None,
                 packet_id=None, transaction_id=None,
                 date=None,
                 additional_data={}, in_reply_to=None,
                 client_state=None, client_json=None,
                 remote_site_name=None, local_site_name=None,
                 originating_site_name=None, outgoing_flag=None,
                 transaction_state=None, packet_state=None,
                 _original_data=None,
                 **kwargs):
        # Set up empty data dicts
        self._required_data = dict()
        self._allowed_data = dict()

        self.packet_rec_id = int(packet_rec_id) if packet_rec_id is not None else None
        self.packet_id = int(packet_id) if packet_id is not None else None
        self.trans_rec_id = int(trans_rec_id) if trans_rec_id is not None else None
        self.transaction_id = int(transaction_id) if transaction_id is not None else None
        self.local_site_name = str(local_site_name) if local_site_name is not None else None
        self.remote_site_name = str(remote_site_name) if remote_site_name is not None else None
        self.originating_site_name = str(originating_site_name) if originating_site_name is not None else None
        self.outgoing_flag = outgoing_flag if outgoing_flag is not None else None
        # TODO make sure these states are valid amie states
        self.transaction_state = str(transaction_state) if transaction_state is not None else None
        self.client_state = str(client_state) if client_state is not None else None
        self.packet_state = str(packet_state) if packet_state is not None else None

        # This one is a property with special...properties. See client_json() 
        # below for details.
        self.client_json = client_json

        # Optionally, save the origininal version of the packet, usually
        # meaning the JSON we got from the server
        self._original_data = _original_data

        self.additional_data = additional_data
        if date is not None:
            self.date = dtparse(date)
        else:
            self.date = None

        if in_reply_to is None or isinstance(in_reply_to, int):
            # If we're given a string, or None, just use that.
            self.in_reply_to_id = in_reply_to
        elif isinstance(in_reply_to, str):
            # If it's a string, make it an int
            self.in_reply_to_id = int(in_reply_to)
        elif hasattr(in_reply_to, 'packet_rec_id'):
            # If we're given a packet object, get the ID
            self.in_reply_to_id = in_reply_to.packet_rec_id
        elif in_reply_to.get('header', {}).get('packet_rec_id'):
            # If we're given a dict-like object, get the ID from the header
            self.in_reply_to_id = in_reply_to['header']['packet_rec_id']

        for key, value in kwargs.items():
            if key in self._data_keys_required or key in self._data_keys_allowed:
                if 'Date' in key:
                    # TODO check if this is a valid assumption
                    setattr(self, key, dtparse(value))
                else:
                    setattr(self, key, value)
            else:
                self.additional_data[key] = value

    @property
    def client_json(self):
        return self._client_json

    @client_json.setter
    def client_json(self, input_json):
        """
        If we're given a string for client_json, assume it's json and
        parse it
        """
        if isinstance(input_json, str):
            self._client_json = json.loads(input_json)
        else:
            self._client_json = input_json

    @classmethod
    def _find_packet_type(cls, packet_or_packet_type):
        """
        Finds the class for the given packet or packet type
        """
        pkt_cls = None
        if type(packet_or_packet_type) == str:
            # We're given a string, search in
            # subclasses
            for subclass in Packet.__subclasses__():
                if subclass._packet_type == packet_or_packet_type:
                    pkt_cls = subclass
                    break
        elif packet_or_packet_type.__class__ in Packet.__subclasses__():
            # We've been given a packet, just get its class attribute
            pkt_cls = packet_or_packet_type.__class__

        if pkt_cls is None:
            # Raise a NotImplementedError if we can't find a subclass
            error_str = "No packet type matches provided '{}'".format(packet_or_packet_type)
            raise PacketInvalidType(error_str)
        return pkt_cls

    @classmethod
    def from_dict(cls, data):
        """
        Generates an instance of an AMIE packet of this type from provided dictionary

        Args:
            data (dict): Packet data
        """
        # Get the subclass that matches this json input
        pkt_class = cls._find_packet_type(data['type'])

        obj = pkt_class(packet_rec_id=data['header']['packet_rec_id'],
                        trans_rec_id=data['header']['trans_rec_id'],
                        packet_id=data['header']['packet_id'],
                        transaction_id=data['header']['transaction_id'],
                        local_site_name=data['header']['local_site_name'],
                        remote_site_name=data['header']['remote_site_name'],
                        originating_site_name=data['header']['originating_site_name'],
                        outgoing_flag=data['header']['outgoing_flag'],
                        transaction_state=data['header']['transaction_state'],
                        packet_state=data['header']['packet_state'],
                        in_reply_to=data['header'].get('in_reply_to'),
                        client_state=data['header'].get('client_state'),
                        client_json=data['header'].get('client_json'),
                        _original_data=data,
                        **data['body'])

        # Return an instance of the proper subclass
        return obj

    @classmethod
    def from_json(cls, json_string):
        """
        Generates an instance of an AMIE packet of this type from provided JSON.
        Basically just a wrapper around from_dict.

        Args:
            json_string (string): JSON data
        """
        data = json.loads(json_string)
        return cls.from_dict(data)

    def reply_packet(self, packet_rec_id=None, packet_type=None, force=False):
        """
        Returns a packet that the current packet would expect as a response,
        with the in_reply_to attribute set to the current packet's ID.

        Generally, most packets only have one kind of expected reply,
        so you should be fine to use reply_packet with just the desired packet_rec_id

        Args:
            packet_rec_id: The ID of the reply packet, if needed
            packet_type: Optionally, the type of the reply packet
            force: will create a reply packet whether or not packet_type is in _expected_reply

        Example:
            >>> my_npc = received_rpc.reply_packet()
        """

        expected_replies = [r['type'] for r in self.expected_reply]
        if packet_type and force:
            # Just do it
            pkt_class = self._find_packet_type(packet_type)
        elif len(expected_replies) == 0:
            # This is a packet that does not expect a response
            raise PacketInvalidType("Packet type '{}' does not expect a reply"
                                    .format(self._packet_type))
        elif len(expected_replies) > 1 and packet_type is None:
            # We have more than one expected reply, but no spec'd type
            # to disambiguate
            raise PacketInvalidType("Packet type '{}' has more than one"
                                    " expected response. Specify a packet type"
                                    " for the reply".format(self._packet_type))
        elif packet_type is not None and packet_type not in expected_replies:
            raise PacketInvalidType("'{}' is not an expected reply for packet type '{}'"
                                    .format(packet_type, self._packet_type))
        else:
            # We have one packet type, or a specified packet type, and it is valid
            if packet_type is None:
                packet_type = expected_replies[0]
            pkt_class = self._find_packet_type(packet_type)
        return pkt_class(packet_rec_id=packet_rec_id, in_reply_to=self.packet_rec_id)

    def as_dict(self):
        """
        This packet, as a dictionary.
        """
        data_body = {}
        # Filter out non-defined items from our data collections, converting
        # if neccessary
        for d in [self._required_data, self._allowed_data, self.additional_data]:
            for k, v in d.items():
                if type(v) == datetime:
                    data_body[k] = v.isoformat()
                elif v is not None:
                    data_body[k] = v

        header = {
            'packet_rec_id': self.packet_rec_id,
            'packet_id': self.packet_id,
            'transaction_id': self.packet_rec_id,
            'trans_rec_id': self.trans_rec_id,
            'expected_reply_list': self._expected_reply,
            'local_site_name': self.local_site_name,
            'remote_site_name': self.remote_site_name,
            'originating_site_name': self.originating_site_name,
            'outgoing_flag': self.outgoing_flag,
            'transaction_state': self.transaction_state,
            'packet_state': self.packet_state,
        }
        if self.date is not None:
            header['date'] = self.date.isoformat()
        if self.in_reply_to_id:
            header['in_reply_to'] = self.in_reply_to_id
        if self.client_state:
            header['client_state'] = self.client_state
        if self.client_json:
            header['client_json'] = self.client_json
        data_dict = {
            'DATA_TYPE': 'packet',
            'type': self.packet_type,
            'body': data_body,
            'header': header
        }

        return data_dict

    def missing_attributes(self):
        """
        Returns a list of attributes that need to be filled out by the user in
        order for this packet to be valid.
        """
        if self.in_reply_to_id:
            reqd = list(set(self._data_keys_required)
                        - set(self._data_keys_not_required_in_reply))
        else:
            reqd = self._data_keys_required

        missing = [r for r in reqd if self._required_data.get(r) is None]
        return missing

    def json(self, **json_kwargs):
        """
        The JSON representation of this AMIE packet
        """
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def validate_data(self, raise_on_invalid=False):
        """
        By default, checks to see that all required data items have a
        defined value, unless in_reply_to is not None (in which case,
        we assume the missing data will be filled in based on the referenced
        packet ID.

        Some packet types will override this function, or add additional checks.
        """
        for k, v in self._required_data.items():
            # If this is a packet in reply to another, and this key is one that
            # the server can infer, skip it.
            if (self.in_reply_to_id and
               k in self._data_keys_not_required_in_reply):
                continue
            # Otherwise, throw an error or return false.
            elif v is None:
                if raise_on_invalid:
                    raise PacketInvalidData('Missing required data field: "{}"'.format(k))
                else:
                    return False
        return True

    @property
    def packet_type(self):
        """
        The AMIE name for this packet type.
        """
        return self._packet_type
