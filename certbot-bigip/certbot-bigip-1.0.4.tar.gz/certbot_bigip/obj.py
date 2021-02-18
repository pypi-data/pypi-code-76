'''Module contains classes used by the F5 BIG-IP Configurator.'''

import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import os
import string
import logging

from acme import challenges

from certbot import errors
from certbot import interfaces
from certbot import reverter
from certbot import util

from certbot.plugins import common

from collections import defaultdict

from f5.bigip import ManagementRoot
from f5.multi_device.device_group import DeviceGroup
from f5.bigip.contexts import TransactionContextManager

# this is just really annoying
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)


class Bigip(object):
    ''' Object representing a single F5 BIG-IP system

    Function list:
        def __init__(self, hosts, port, username, password, device_group, partition='Common', verify_certificate=False, clientssl_parent='/Common/clientssl', apm=False):
        def __str__(self):
        def _split_fullpath(self, fullpath):
        def get_version(self):
        def active(self):
        def save(self):
        def save_ucs(self, ucs_name):
        def upload_file(self, local_file_name):
        def exists_crypto_cert(self, certificate):
        def exists_crypto_key(self, key):
        def update_crypto(self, domain, cert, key, chain):
        def create_crypto_cert(self, domain, cert):
        def create_crypto_key(self, domain, key):
        def exists_clientssl_profile(self, domain, virtual_name):
        def create_clientssl_profile(self, domain, virtual_name, iapp):
        def exists_irule(self, irule_name):
        def create_irule_HTTP01(self, token, http_response_content):
        def delete_irule(self, token):
        def exists_virtual(self, virtual_name):
        def profile_on_virtual(self, virtual_name, profile_type):
        def http_virtual(self, virtual_name):
        def client_ssl_virtual(self, virtual_name):
        def associate_client_ssl_virtual(self, virtual_name, client_ssl_name):
        def irules_on_virtual(self, virtual_name):
        def associate_irule_virtual(self, token, virtual_name):
        def remove_irule_virtual(self, token, virtual_name):

    '''
    # INIT - Funktion

    def __init__(self, hosts, port, username, password, device_group, partition='Common', verify_certificate=False, clientssl_parent='/Common/clientssl', apm=False):
        self.hosts = hosts
        self.port = port
        self.username = username
        self.__password = password
        self.token = True
        self.partition = partition
        self.device_group = device_group
        self.clientssl_parent = clientssl_parent
        self.valid = False
        self.version = 'UNKNOWN'
        self.apm = apm

        try:
            self.mgmt = ManagementRoot(self.hosts[0], self.username, self.__password, token=True)
        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'
                   '(You most probably need to ensure the username and'
                   'password is correct. Make sure you use the --bigip-username'
                   'and --bigip-password options)'.format(self.hosts[0], e, os.linesep))
            raise errors.AuthorizationError(msg)

    def __str__(self):
        return '{0}@{1}:{2}'.format(self.username, self.host, self.port)

    ############################################
    ############ Helper Functions ##############
    ############################################

    def _split_fullpath(self, fullpath):
        try:
            '''Return partition, subpath and name from object.'''
            if len(fullpath.split('/')) == 4:
                subpath = fullpath.split('/')[2]
                partition = fullpath.split('/')[1]
                name = fullpath.split('/')[3]
            elif len(fullpath.split('/')) == 3:
                subpath = ''
                partition = fullpath.split('/')[1]
                name = fullpath.split('/')[2]
            elif len(fullpath.split('/')) == 2:
                subpath = ''
                partition = 'Common'
                name = fullpath.split('/')[2]

            return [partition, subpath, name]
        except Exception as e:
            msg = ('Failure with {0}.{2}'
                   'Error raised was {2}{1}{2}'.format(fullpath, e, os.linesep))
            raise errors.PluginError(msg)

    def get_version(self):
        return 'N/A'

    def active(self):
        ''' Return true if active for any of the traffic groups which virtual servers (self.bigip_vs_list) are within'''

        return True

    ############################################
    ############ Ablauf Funktionen #############
    ############################################
    # 1. Probiere eine Connection zu jeder F5
    # 2. Überprüfen, welche der F5s die aktive ist
    # 3. Upload der Zertifikate auf die aktive F5
    # 4. Überprüfen, ob es Zertifikate mit dem sleben Namen gibt
    # 5. Updaten / Erstellen der neuen Zertifikate
    # 6. Überprüfune ob es bereits ein SSL Profil gibt
    # 7. SSl Profil updaten / neu erstellen
    # 8. SSL Profile dem Virtuelle Server zuweisen

    def save(self):
        try:
            self.mgmt.tm.sys.config.exec_cmd('save')
            list_of_bigips = []
            for bigip in self.hosts:
                list_of_bigips.append(ManagementRoot(bigip, self.username, self.__password))

            device_group = DeviceGroup(devices=list_of_bigips, device_group_name=self.device_group,
                                       device_group_type='sync-failover', device_group_partition='Common')
            device_group.ensure_all_devices_in_sync()

        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.PluginError(msg)

    def save_ucs(self, ucs_name):
        try:
            self.mgmt.tm.sys.ucs.exec_cmd('save', name=ucs_name)
            return True

        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.PluginError(msg)

    def upload_file(self, local_file_name):
        try:
            self.mgmt.shared.file_transfer.uploads.upload_file(local_file_name)
            return True

        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.CertStorageError(msg)

    def exists_crypto_cert(self, certificate):
        try:
            return self.mgmt.tm.sys.file.ssl_certs.ssl_cert.exists(
                name='{0}_Letsencrypt'.format(certificate), partition=self.partition)

        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.CertStorageError(msg)

    def exists_crypto_key(self, key):
        try:
            return self.mgmt.tm.sys.file.ssl_keys.ssl_key.exists(
                name='{0}_Letsencrypt'.format(key), partition=self.partition)

        except Exception as e:
            raise BigIpCertStorageError(self.hosts[0], e)

    def update_crypto(self, name, cert, key, chain, cert_chain_name):
        # Because they exist, we will modify them in a transaction
        # deprecated
        try:
            tx = self.mgmt.tm.transactions.transaction
            with TransactionContextManager(tx) as api:

                self._update_crypto_key(api, key, name)
                self._update_crypto_cert(api, cert, name)

            self._update_crypto_cert(api, chain, cert_chain_name)

        except Exception as e:
            raise BigIpCertStorageError(self.hosts[0],e)

    def _update_crypto_cert(self, api, cert, name):
        if self.exists_crypto_cert(name):
            logger.debug(f"updating cert for {name}")
            modcert = api.tm.sys.file.ssl_certs.ssl_cert.load(
                name='{0}_Letsencrypt'.format(name), partition=self.partition)
            modcert.sourcePath = 'file:/var/config/rest/downloads/{0}'.format(
                os.path.basename(cert))
            modcert.update()

        else:
            logger.debug(f"creating cert for {name}")
            modcert = self.mgmt.tm.sys.file.ssl_certs.ssl_cert.create(
                name='{0}_Letsencrypt'.format(name), partition=self.partition,
                sourcePath='file:/var/config/rest/downloads/{0}'.format(os.path.basename(cert)))

    def _update_crypto_key(self, api, key, name):
        if self.exists_crypto_key(name):
            logger.debug(f"updating key for {name}")
            modkey = api.tm.sys.file.ssl_keys.ssl_key.load(
                name='{0}_Letsencrypt'.format(name), partition=self.partition)
            modkey.sourcePath = 'file:/var/config/rest/downloads/{0}'.format(
                os.path.basename(key))
            modkey.update()
        else:
            logger.debug(f"creating key for {name}")
            modkey = self.mgmt.tm.sys.file.ssl_keys.ssl_key.create(
                name='{0}_Letsencrypt'.format(name), partition=self.partition,
                sourcePath='file:/var/config/rest/downloads/{0}'.format(os.path.basename(key)))

    def exists_clientssl_profile(self, domain, virtual_name, iapp):
        try:
            r = self._split_fullpath(virtual_name)
            name = '{0}_clientssl'.format(domain)
            if iapp != '':
                return self.mgmt.tm.ltm.profile.client_ssls.client_ssl.exists(
                    name=name, partition=self.partition, subPath=r[1])
            else:
                return self.mgmt.tm.ltm.profile.client_ssls.client_ssl.exists(name=name, partition=self.partition)

        except Exception as e:
            msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.CertStorageError(msg)

    def update_clientssl_profile(self, domain, virtual_name, iapp):
        if "wildcard" not in domain:
            wildcard = False
        else:
            wildcard = True
        if not self.exists_clientssl_profile(domain, virtual_name, iapp):
            self.create_clientssl_profile(domain, virtual_name, iapp, wildcard)
        else:
            logger.debug("Nothing left to do")
            # self.associate_client_ssl_to_virtual(domain, virtual_name)
            # logger.debug("SSL profile added to virtual Server")

    def create_clientssl_profile(self, domain, virtual_name, iapp, wildcard):

        # Lege ein Client SSL Profil in der richtigen Partition und Pfad an
        # Wenn es sich um ein Wildcard Zertifikat handelt, lege es als Default SNI Profil an

        sni_default = wildcard

        try:
            r = self._split_fullpath(virtual_name)
            if iapp != '':
                name = '/{0}/{1}/{2}_clientssl'.format(self.partition, r[1], domain)
            else:
                name = '/{0}/{1}_clientssl'.format(self.partition, domain)
            cssl_profile = {
                'name': name,
                'cert': '/{0}/{1}_Letsencrypt'.format(self.partition, domain),
                'key': '/{0}/{1}_Letsencrypt'.format(self.partition, domain),
                'chain': '/{0}/chain_Letsencrypt'.format(self.partition),
                'defaultsFrom': self.clientssl_parent,
                'app-service': iapp,
                'sniDefault': sni_default
            }
            self.mgmt.tm.ltm.profile.client_ssls.client_ssl.create(**cssl_profile)
            return True

        except Exception as e:
            msg = ('Certificate creation on F5 Failed. Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                   'Error raised was {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.CertStorageError(msg)

    def associate_client_ssl_to_virtual(self, domain, virtual_name):
        try:
            r = self._split_fullpath(virtual_name)
            ssl_profile_name = '{0}{1}_clientssl'.format(virtual_name[:virtual_name.rfind("/")+1], domain)
            virtual_server = self.mgmt.tm.ltm.virtuals.virtual.load(partition=r[0], subPath=r[1], name=r[2])
            virtual_server.profiles_s.profiles.create(partition=r[0], name=ssl_profile_name)

        except Exception as e:
            msg = ('Association of SSL Profile with Virtual server failed. {0}', format(e))
            raise errors.ConfigurationError(msg)

    def exists_irule(self, irule_name):
        try:
            return self.mgmt.tm.ltm.rules.rule.exists(partition=self.partition, name=irule_name)

        except Exception as e:
            msg = ('iRule creation on {0} failed. {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def create_irule_HTTP01(self, token, http_response_content, apm):
        try:
            irule_name = 'Certbot-Letsencrypt-{0}'.format(token)
            if apm is True:
                irule_text = 'when CLIENT_ACCEPTED {{\n  catch {{\n    ACCESS::restrict_irule_events disable\n  }}\n}}\nwhen HTTP_REQUEST priority 100 {{\n  if {{[HTTP::has_responded]}}{{return}}\n  if {{[HTTP::uri] equals \"/.well-known/acme-challenge/{0}\"}} {{\n    HTTP::respond 200 -version auto content \"{1}\" noserver \n  }}\n}}'.format(
                    token, http_response_content)
            else:
                irule_text = 'when HTTP_REQUEST priority 100 {{\n  if {{[HTTP::has_responded]}}{{return}}\n  if {{[HTTP::uri] equals \"/.well-known/acme-challenge/{0}\"}} {{\n    HTTP::respond 200 -version auto content \"{1}\" noserver \n  }}\n}}'.format(
                    token, http_response_content)

            resp = self.mgmt.tm.ltm.rules.rule.create(
                name=irule_name, partition=self.partition, apiAnonymous=irule_text)
            return True

        except Exception as e:
            msg = ('iRule creation on {0} failed. {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def delete_irule(self, token):
        try:
            irule_name = 'Certbot-Letsencrypt-{0}'.format(token)

            rule = self.mgmt.tm.ltm.rules.rule.load(name=irule_name, partition=self.partition)
            rule.delete()
            return True

        except Exception as e:
            msg = ('iRule deletion from {0} failed. {2}{1}{2}'.format(self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def exists_virtual(self, virtual_name):
        try:
            r = self._split_fullpath(virtual_name)
            return self.mgmt.tm.ltm.virtuals.virtual.exists(partition=r[0], subPath=r[1], name=r[2])

        except Exception as e:
            msg = ('Virtual server {3} check on {0} failed. {2}{1}{2}'.format(
                self.hosts[0], e, os.linesep, virtual_name))
            raise errors.ConfigurationError(msg)

    def profile_on_virtual(self, virtual_name, profile_type):
        try:
            r = self._split_fullpath(virtual_name)
            virtual = self.mgmt.tm.ltm.virtuals.virtual.load(
                partition=r[0], subPath=r[1], name=r[2])

            if virtual != '':
                for profile in virtual.profiles_s.get_collection():
                    r = self._split_fullpath(profile.fullPath)
                    try:
                        getattr(getattr(getattr(self.mgmt.tm.ltm.profile, '{0}s'.format(profile_type)), '{0}'.format(
                            profile_type)), 'load')(partition=r[0], subPath=r[1], name=r[2])
                        return True
                    except:
                        pass
                return False
            else:
                return False

        except Exception as e:
            msg = ('Test for HTTP profile on virtual server on {0} failed. {2}{1}{2}'.format(
                self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def http_virtual(self, virtual_name):
        return self.profile_on_virtual(virtual_name, 'http')

    def client_ssl_virtual(self, virtual_name):
        return self.profile_on_virtual(virtual_name, 'client_ssl')

    def irules_on_virtual(self, virtual_name):
        try:
            r = self._split_fullpath(virtual_name)
            virtual = self.mgmt.tm.ltm.virtuals.virtual.load(
                partition=r[0], subPath=r[1], name=r[2])

            if virtual != '' and 'rules' in virtual.raw:
                return {'result': True, 'rules': virtual.rules}
            else:
                return {'result': False, 'rules': []}

        except Exception as e:
            msg = ('Retrieval of iRules for virtual server on {0} failed. {2}{1}{2}'.format(
                self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def associate_irule_virtual(self, token, virtual_name):
        try:
            r = self._split_fullpath(virtual_name)
            irules = self.irules_on_virtual(virtual_name)
            virtual = self.mgmt.tm.ltm.virtuals.virtual.load(
                partition=r[0], subPath=r[1], name=r[2])
            if irules['result'] == True:
                virtual.rules.append('/{0}/Certbot-Letsencrypt-{1}'.format(self.partition, token))
            else:
                virtual.rules = ['/{0}/Certbot-Letsencrypt-{1}'.format(self.partition, token)]
            virtual.update()
            return True

        except Exception as e:
            msg = ('iRule association to virtual server on {0} failed. {2}{1}{2}'.format(
                self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)

    def remove_irule_virtual(self, token, virtual_name):
        try:
            r = self._split_fullpath(virtual_name)
            irules = self.irules_on_virtual(virtual_name)
            if irules['result'] is True:
                virtual = self.mgmt.tm.ltm.virtuals.virtual.load(
                    partition=r[0], subPath=r[1], name=r[2])
                if '/{0}/Certbot-Letsencrypt-{1}'.format(self.partition, token) in virtual.rules:
                    virtual.rules.remove('/{0}/Certbot-Letsencrypt-{1}'.format(self.partition, token))
                    virtual.update()
            return True

        except Exception as e:
            msg = ('iRule removal from virtual server on {0} failed. {2}{1}{2}'.format(
                self.hosts[0], e, os.linesep))
            raise errors.ConfigurationError(msg)


class BigIpCertStorageError(errors.CertStorageError):
    def __init__(self, host: str, e: Exception):
        self.  msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                      'Error raised was {2}{1}{2}'.format(host, e, os.linesep))
