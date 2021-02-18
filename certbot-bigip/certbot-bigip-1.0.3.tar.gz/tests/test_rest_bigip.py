import logging
import subprocess

from certbot_bigip.configurator import BigipConfigurator
from certbot_bigip.obj import Bigip
import time
import logging
import re
import socket
import ssl
import os

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)
user = os.environ['BIGIP_USERNAME']
password = os.environ['BIGIP_PASSWORD']

# Instanciating an object without using the certbot-CLI #
#########################################################

# class Config(object):
#     def __init__(self):
#         self.certbot_bigip_list ='f5.ong.intern,f5-ha.ong.intern'
#         self.certbot_bigip_username = f'{user}'
#         self.certbot_bigip_password = f'{password}'
#         self.certbot_bigip_partition = 'Intern'
#         self.certbot_bigip_iapp = '/Intern/certbot.ong.at.app/certbot.ong.at'
#         self.certbot_bigip_clientssl_parent = "/Common/ong_clientssl"
#         self.certbot_bigip_vs_list = '/Intern/certbot.ong.at.app/certbot.ong.at_vs'
#         self.certbot_bigip_device_group = 'fail-sync'
#         self.certbot_bigip_apm=False
#         self.backup_dir = "/tests/backup"
#         self.strict_permissions = False
#         self.temp_checkpoint_dir = "/tests/backup"
#         self.in_progress_dir = "/tests/backup"

# def test_upload_cert_to_bigip():
#     config = Config()

#     configurator = BigipConfigurator(config, "certbot_bigip")
#     configurator.prepare()

#     domain = "*.flo.certbot.ong.at"
#     cert_path = "/builds/infra/certbot-plugins/certbot-bigip-plugin/tests/test_certificates/test_certbot_ong_at.pem"
#     key_path = "/builds/infra/certbot-plugins/certbot-bigip-plugin/tests/test_certificates/test_certbot_ong_at_key.pem"
#     chain_path = "/builds/infra/certbot-plugins/certbot-bigip-plugin/tests/test_certificates/test_chain.pem"
#     if configurator.deploy_cert(domain,cert_path,key_path,chain_path,):
#         assert True

