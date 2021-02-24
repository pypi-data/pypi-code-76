# Created by Antonio Di Mariano (antonio.dimariano@gmail.com) at 04/02/2021
from service_configuration_controller.helpers.decode_messages import decode_incoming_msg
import unittest


class TestWriteData(unittest.TestCase):

    def test_a_decode_a_json_message(self):
        message = {'service_name': 'my-service-name', 'timestamp': '2021-02-05T15:15:02+00:00',
                   'start_environment': 'production', 'datacentre': '{}',
                   'external_rest_services': '{"repository_url": "http://repository:3000/api/"}',
                   'persistence_conf': '{}',
                   'credentials': '{"authenticated_user_data": {"id": "su-user@xxx.com", "domain": "xxx", "email": "su-user@xxx.com"}}'}
        decoded_version = {'service_name': 'my-service-name', 'timestamp': '2021-02-05T15:15:02+00:00', 'start_environment': 'production', 'datacentre': {}, 'external_rest_services': {'repository_url': 'http://repository:3000/api/'}, 'persistence_conf': {}, 'credentials': {'authenticated_user_data': {'id': 'su-user@xxx.com', 'domain': 'xxx', 'email': 'su-user@xxx.com'}}}
        ret = decode_incoming_msg(message=message)
        self.assertEqual(ret, decoded_version)

    def test_b_return_the_same_json_version(self):
        decoded_version = {'service_name': 'my-service-name', 'timestamp': '2021-02-05T15:15:02+00:00', 'start_environment': 'production', 'datacentre': {}, 'external_rest_services': {'repository_url': 'http://repository:3000/api/'}, 'persistence_conf': {}, 'credentials': {'authenticated_user_data': {'id': 'su-user@xxx.com', 'domain': 'xxx', 'email': 'su-user@xxx.com'}}}
        ret = decode_incoming_msg(message=decoded_version)
        self.assertEqual(ret, decoded_version)
