'''Certbot Bigip plugin.'''
import sys
import time
import os
import logging

import certbot
import zope.interface

from acme import challenges

from certbot import errors
from certbot import interfaces

from certbot.plugins import common

from . import constants
from . import obj

from collections import defaultdict



# Logging
path = "/var/log/bigip"
os.makedirs(path, exist_ok=True)
filehandler = logging.FileHandler(path+"/bigip.log")
filehandler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('[%(asctime)s] [%(levelname)8s] [%(name)30s] %(message)s')
filehandler.setFormatter(formatter)

streamhandler=logging.StreamHandler()
streamhandler.setLevel(logging.DEBUG)

logging.getLogger("certbot_bigip").addHandler(streamhandler)
logging.getLogger("certbot_bigip").addHandler(filehandler)
logger = logging.getLogger(__name__)


# Define a helper function to avoid verbose code
z_util = zope.component.getUtility


@zope.interface.implementer(interfaces.IAuthenticator, interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class BigipConfigurator(common.Plugin):
    '''F5 BIG-IP Configurator'''

    description = 'F5 BIG-IP - experimental!'

    @classmethod
    def add_parser_arguments(cls, add):
        add('list', metavar='bigip1,bigip2', default=constants.CLI_DEFAULTS['bigip_list'],
            help='CSV list of BIG-IP system hostnames or addresses, all have to be in the same cluster')
        add('username', metavar='USERNAME', default=constants.CLI_DEFAULTS['bigip_username'],
            help='BIG-IP username (common to all listed BIG-IP systems)')
        add('password', metavar='PASSWORD', default=constants.CLI_DEFAULTS['bigip_password'],
            help='BIG-IP password (common to all listed BIG-IP systems)')
#        add('password-env', metavar='VARIABLE_NAME', default=constants.CLI_DEFAULTS['bigip_password_env'],
#            help='Evnironment variable for BIG-IP password')
#        add('password-file', metavar='/path/to/file', default=constants.CLI_DEFAULTS['bigip_password_file'],
#            help='File to read for BIG-IP password')
        add('partition', metavar='PartitionName', default=constants.CLI_DEFAULTS['bigip_partition'],
            help='BIG-IP partition (common to all listed BIG-IP systems)')
        add('iapp', metavar='Application Service Name', default=constants.CLI_DEFAULTS['bigip_iapp'],
            help='BIG-IP partition (common to all listed BIG-IP systems)')
        add('vs-list', metavar='vs1,vs2,vs3', default=constants.CLI_DEFAULTS['virtual_server_list'],
            help='CSV list of BIG-IP virtual server names, optionally including partition')
        add('ciphers', metavar='CIPHER_STRING', default=constants.CLI_DEFAULTS['bigip_ciphers'],
            help='Cipher list for client SSL profile (will not inherit from parent profile)')
        add('clientssl-parent', metavar='/Partition/Profile', default=constants.CLI_DEFAULTS['bigip_clientssl_parent'],
            help='Client SSL parent profile to inherit default values from')
        add('device-group', metavar='sync-failover', default=constants.CLI_DEFAULTS['bigip_device_group'],
            help='Device Group to syncronise configuration')
        add('apm', metavar='apm', default=constants.CLI_DEFAULTS['bigip_apm'],
            help='Is the VS APM enabled or not')
#        add('convert-http', metavar='True|False', default=False,
#            help='Convert HTTP virtual servers to HTTPS virtual servers')
#        add('clone-http', metavar='True|False', default=False,
#            help='Clone HTTP virtual servers to HTTPS virtual servers')

    def __init__(self, *args, **kwargs):
        '''Initialize an F5 BIG-IP Configurator'''

        version = kwargs.pop('version', None)
        super(BigipConfigurator, self).__init__(*args, **kwargs)

        # Add name_server association dict
        self.assoc = dict()
        # Outstanding challenges
        self._chall_out = set()
        # Maps enhancements to vhosts we've enabled the enhancement for
        self._enhanced_vhosts = defaultdict(set)

        self.bigip_list = []
        self.bigip_vs_list = []
        self.apm = False

        self.version = version
        self.vservers = None
        self._enhance_func = {}

        # self.reverter = reverter.Reverter(self.config)

        self._domain = None
        self.cert_chain_name = None

    def prepare(self):
        '''Prepare the authenticator/installer'''

        if self.conf('username') == '':
            msg = ('No username specified, please use --bigip-username')
            raise errors.MissingCommandlineFlag(msg)

        if self.conf('password') == '':
            msg = ('No password specified, please use --bigip-password')
            raise errors.MissingCommandlineFlag(msg)

        if self.conf('vs_list') != '' and self.conf('vs_list') is not None:
            self.bigip_vs_list = self.conf('vs_list').split(',')
            for vs in self.bigip_vs_list:
                logger.debug('Virtual server: {0}'.format(vs))
        else:
            msg = ('--bigip-vs-list is required when using the F5 BIG-IP plugin')
            raise errors.MissingCommandlineFlag(msg)

        self.iapp = ''
        if self.conf('iapp') != '' and self.conf('iapp') is not None:
            self.iapp = self.conf('iapp')

        if self.conf('list') != '':
            self.bigip_host_list = self.conf('list').split(',')
            try:
                self.bigip = obj.Bigip(self.bigip_host_list, 443, self.conf('username'), self.conf(
                    'password'), self.conf('device-group'), self.conf('partition'), False, self.conf('clientssl-parent'))
            except Exception as e:
                msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                       'Error raised was {2}{1}{2}'
                       '(You most probably need to ensure the username and'
                       'password is correct. Make sure you use the --bigip-username'
                       'and --bigip-password options)'.format(self.bigip_host_list[0], e, os.linesep))
                raise errors.AuthorizationError(msg)
        else:
            msg = ('--bigip-list is required when using the F5 BIG-IP plugin')
            raise errors.MissingCommandlineFlag(msg)
        if "--staging" in sys.argv:
            self.cert_chain_name = "staging_chain"
            logger.debug("certbot was called in staging mode")
        else:
            self.cert_chain_name = "chain"
        
        if self.conf('apm'):
            self.apm = True

    def config_test(self):

        logger.debug('in config_test()')

        return

    def more_info(self):
        '''Human-readable string to help understand the module'''

        return (
            'Configures F5 BIG-IP to authenticate and configure X.509'
            'certificate/key use. Only one F5 Cluster addressable.'
        )

    def get_chall_pref(self, domain):
        '''Return list of challenge preferences.'''

        return [challenges.HTTP01]
        # TODO: support TLSSNI01
        # return [challenges.TLSSNI01]

    def perform(self, achalls):
        '''Perform the configuration related challenge.

        This function currently assumes all challenges will be fulfilled.
        If this turns out not to be the case in the future. Cleanup and
        outstanding challenges will have to be designed better.

        '''

        responses = [None] * len(achalls)

        #tlssni01_chall_doer = tls_sni_01.BigipTlsSni01(self)

        for count, achall in enumerate(achalls):
            if isinstance(achall.chall, challenges.HTTP01):
                response, validation = achall.response_and_validation()
                token = achall.chall.encode('token')
                responses[count] = response

                bigip = self.bigip
                if not bigip.exists_irule('Certbot-Letsencrypt-{0}'.format(token)):
                    bigip.create_irule_HTTP01(token, validation, self.apm)

                logger.debug('DEBUG: VS-List: {0}'.format(self.bigip_vs_list))
                for virtual_server in self.bigip_vs_list:
                    logger.debug('DEBUG: VS: {0}'.format(virtual_server))
                    try:
                        if bigip.exists_virtual(virtual_server) and bigip.http_virtual(virtual_server):
                            # virtual server exists and has a HTTP profile attached to it
                            # associate the iRule to it which will respond for HTTP01 validations
                            logger.debug('Associating irule with {0}'.format(virtual_server))
                            bigip.associate_irule_virtual(token, virtual_server)
                            time.sleep(10)
                        else:
                            logger.debug(
                                'VS {0} does not exist or has no HTTP profile attached. Skipping challenge on this VS'.format(virtual_server))
                    except Exception as e:
                        msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                               'Error raised was {2}{1}{2}'.format(self.bigip_host_list[0], e, os.linesep))
                        raise errors.PluginError(msg)

        return responses

    def cleanup(self, achalls):
        '''Revert all challenges.'''

        for achall in achalls:
            if isinstance(achall.chall, challenges.HTTP01):
                token = achall.chall.encode('token')
                for virtual_server in self.bigip_vs_list:
                    if self.bigip.exists_virtual(virtual_server):
                        if self.bigip.remove_irule_virtual(token, virtual_server) != True:
                            logger.error('iRule could not be removed from virtual server {0} you may need to do this manually'.format(
                                virtual_server))
                    else:
                        logger.error(
                            'The virtual server {0} does not appear to exist on this BIG-IP'.format(virtual_server))
                try:
                    self.bigip.delete_irule(token)
                except Exception as e:
                    msg = ('Connection to F5 BIG-IP iControl REST API on {0} failed.{2}'
                           'Error raised was {2}{1}{2}'.format(self.bigip_host_list[0], e, os.linesep))
                    raise errors.PluginError(msg)
            elif isinstance(achall.chall, challenges.DNS01):
                pass # Nothing to do, keine Änderungen für Challenge auf F5

        return

    def get_all_names(self):
        '''Cannot currently work for F5 BIG-IP due to the way in which Cerbot validates
        returned strings as conforming to host/domain name format. e.g. F5 BIG-IP virtual
        server names are not always in pure host/domain name.

        :raises errors.PluginError: Always

        '''

        msg = ('Certbot can\'t be used to select domain names based on F5 '
               'BIG-IP Virtual Server names.{0}{0}Please use CLI arguments, '
               'example: --bigip-vs-list virtual_name1,virtual_name2 --domain '
               'domain.name'.format(os.linesep))

        raise errors.PluginError(msg)

    def deploy_cert(self, domain, cert_path, key_path, chain_path=None, fullchain_path=None):
        '''Deploys certificate and key to specified F5 BIG-IP, creates or updates
        client SSL profiles, and ensures they are associated with the specified
        virtual server.

        NOTE: This gets run for EVERY primary certificate name and every subjectAltName
              in a certificate. Need to improve efficiency within F5 BIG-IP config by
              not creating lots of duplicates of certs/keys.

        :raises errors.PluginError: When unable to deploy certificate due to
            a lack of directives

        '''
        logger.debug("Deploying on bigip")
        bigip = self.bigip

        logger.debug("Uploading certificates to bigip")
        bigip.upload_file(cert_path)
        bigip.upload_file(key_path)
        bigip.upload_file(chain_path)

        logger.debug("deploying certs and keys on bigip")
        bigip.update_crypto(domain.replace(".", "_").replace("*", "wildcard"), cert_path, key_path, chain_path, self.cert_chain_name)
        logger.debug("Deployed Succesfully")

        logger.debug("Updating Client SSL Profile")

        bigip.update_clientssl_profile(domain.replace(".", "_").replace("*", "wildcard"), self.bigip_vs_list[0], self.iapp)
        logger.debug("Successfully Updated Client SSL Profile")
        # bigip.associate_client_ssl_virtual(self.bigip_vs_list[0],domain.replace(".", "_").replace("*", "wildcard"))
        return True

    def enhance(self, domain, enhancement, options=None):
        '''Enhance configuration.

        :param str domain: domain to enhance
        :param str enhancement: enhancement type defined in
            :const:`~certbot.constants.ENHANCEMENTS`
        :param options: options for the enhancement
            See :const:`~certbot.constants.ENHANCEMENTS`
            documentation for appropriate parameter.

        :raises .errors.PluginError: If Enhancement is not supported, or if
            there is any other problem with the enhancement.

        '''

        logger.debug('DEBUG: enhance(domain={0}, enhancement={1}, options={2})'.format(
            domain, enhancement, options))

        return

    def supported_enhancements(self):  # pylint: disable=no-self-use
        '''Returns currently supported enhancements.'''

        return ['ensure-http-header', 'redirect', 'staple-ocsp']

    def get_all_certs_keys(self):

        logger.debug('DEBUG: in get_all_certs_keys()')

        return []

    def save(self, title=None, temporary=False):
        '''Saves all changes to all F5 BIG-IP's, e.g. tmsh /sys save config.

        This function first checks for save errors, if none are found,
        all configuration changes made will be saved. According to the
        function parameters. If an exception is raised, a new checkpoint
        was not created.

        :param str title: The title of the save. If a title is given, a UCS
            archive will be created.

        :param bool temporary: Indicates whether the changes made will
            be quickly reversed in the future (ie. challenges)

        :raises .errors.PluginError: If there was an error in Augeas, in
            an attempt to save the configuration, or an error creating a
            checkpoint
        '''
        bigip = self.bigip

        if temporary == False:
            bigip.save()

        return

    def revert_challenge_config(self):

        logger.debug('DEBUG: in revert_challenge_config()')

        return

    def rollback_checkpoints(self, rollback=1):

        logger.debug('DEBUG: in rollback_checkpoints()')

        return

    def recovery_routine(self):

        logger.debug('DEBUG: in recovery_routine()')

        return

    def view_config_changes(self):

        logger.debug('DEBUG: in view_config_changes()')

        return

    def restart(self):
        '''Does nothing in context of F5 BIG-IP, but must be defined.

        https://github.com/certbot/certbot/issues/4045
        https://github.com/certbot/certbot/issues/4046
        https://github.com/certbot/certbot/pull/4199#issuecomment-295023089
        As of these events - when certbot renew is called, no installer is called.
        So we need to deploy the new certificates here in the restart function

        '''

        #logger.debug('DEBUG: restart: domain: {0}'.format(self._domain))
        #self.config.live_dir
        #deploy_cert(domain, cert_path, key_path, chain_path=None, fullchain_path=None):

        return
