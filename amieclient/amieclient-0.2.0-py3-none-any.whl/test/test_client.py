from ..client import AMIEClient
from ..packet import RequestAccountCreate, PacketList
from .fixtures import DEMO_JSON_PKT_1, DEMO_JSON_PKT_LIST


class TestAMIEClient:

    def test_creation(self):
        client = AMIEClient(site_name='test', api_key='test')
        assert client._session.headers['XA-SITE'] == 'test'
        assert client._session.headers['XA-API-KEY'] == 'test'

    def test_amie_url(self):
        client1 = AMIEClient(site_name='test', api_key='test',
                             amie_url='http://localhost/amie')
        assert client1.amie_url == 'http://localhost/amie/'
        client2 = AMIEClient(site_name='test', api_key='test',
                             amie_url='http://localhost/amie/')
        assert client2.amie_url == 'http://localhost/amie/'

    def test_get_packet(self, requests_mock):
        client = AMIEClient(site_name='test', api_key='test')

        # Make the mock request
        packet_url = 'https://amieclient.xsede.org/v0.10/packets/test/12345'
        requests_mock.get(packet_url, json=DEMO_JSON_PKT_1)

        packet = client.get_packet(packet_rec_id='12345')
        assert packet.packet_type == 'request_account_create'
        assert isinstance(packet, RequestAccountCreate)

    def test_get_packet_list(self, requests_mock):
        client = AMIEClient(site_name='test', api_key='test')

        # Make the mock request
        packet_url = 'https://amieclient.xsede.org/v0.10/packets/test'
        requests_mock.get(packet_url, json=DEMO_JSON_PKT_LIST)

        r = client.list_packets()
        assert isinstance(r, PacketList)
        assert r.packets[0].packet_type == 'request_account_create'
        assert r.packets[1].packet_type == 'request_account_create'
