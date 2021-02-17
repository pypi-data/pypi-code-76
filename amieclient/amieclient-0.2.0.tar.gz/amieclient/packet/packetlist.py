import json

from .base import Packet


class PacketList(object):
    """
    A list of packets.
    """
    def __init__(self, message=None, packets=None):
        self.message = message
        if packets is not None:
            self.packets = packets
        else:
            self.packets = []

    @classmethod
    def from_dict(cls, dict_in):
        pkt_list = cls(
            message=dict_in.get('message', ''),
            packets=[Packet.from_dict(d) for d in dict_in['result']]
        )
        return pkt_list

    @classmethod
    def from_json(cls, json_in):
        pkt_list_in = json.loads(json_in)
        return cls.from_dict(pkt_list_in)

    def as_dict(self):
        data_dict = {
            'message': self.message,
            'result': [pkt.as_dict()for pkt in self.packets]
        }
        return data_dict

    def json(self, **json_kwargs):
        """
        The JSON representation of these AMIE packets
        """
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))
