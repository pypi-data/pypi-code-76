# -*- coding: UTF-8 -*-
#   Copyright 2009-2021 Oli Schacher, Fumail Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Antiphish / Forging Plugins (DKIM / SPF / SRS etc)

requires: dkimpy (not pydkim!!)
requires: pyspf
requires: pydns (or alternatively dnspython if only dkim is used)
requires: pysrs
requires: pynacl (rare dependeny of dkimpy)
requires: dmarc
"""

from fuglu.shared import ScannerPlugin, apply_template, DUNNO, FileList, string_to_actioncode, get_default_cache, extract_domain, Suspect
from fuglu.extensions.sql import get_session, SQL_EXTENSION_ENABLED
from fuglu.extensions.dnsquery import DNSQUERY_EXTENSION_ENABLED, lookup, QTYPE_TXT
from fuglu.stringencode import force_bString, force_uString
from fuglu.logtools import PrependLoggerMsg
import logging
import os
import re
import time

DKIMPY_AVAILABLE = False
PYSPF_AVAILABLE = False
DMARC_AVAILABLE = False
SRS_AVAILABLE=False

try:
    from dkim import DKIM, sign, Simple, Relaxed, DKIMException, MessageFormatError, ARC, util as dkimutil
    if DNSQUERY_EXTENSION_ENABLED:
        DKIMPY_AVAILABLE = True
except ImportError:
    DKIM = None

try:
    import spf
    if DNSQUERY_EXTENSION_ENABLED:
        PYSPF_AVAILABLE = True
except ImportError:
    spf = None

try:
    from domainmagic.tld import TLDMagic
    DOMAINMAGIC_AVAILABLE = True
except ImportError:
    DOMAINMAGIC_AVAILABLE=False
    TLDMagic = None

try:
    import dmarc
    DMARC_AVAILABLE = True
    if DNSQUERY_EXTENSION_ENABLED and DOMAINMAGIC_AVAILABLE:
        DMARC_AVAILABLE = True
except ImportError:
    dmarc = None

try:
    import SRS
    SRS_AVAILABLE=True
except ImportError:
    SRS=None



ARC_SAHEADER = 'X-ARCVerify'
DKIM_SAHEADER = 'X-DKIMVerify'
DKIM_VALID = 'valid'
DKIM_VALID_AUTHOR = 'validauthor' # dkim record is valid and in authors/from hdr domain
DKIM_VALID_SENDER = 'validsender' # dkim record is valid and in envelope sender domain
DKIM_INVALID = 'invalid'
DKIM_UNSIGNED = 'unsigned'
DMARC_SAHEADER_RESULT = 'X-DMARC-Result'
DMARC_SAHEADER_DISPO = 'X-DMARC-Dispo'
DMARC_REJECT = 'reject'
DMARC_QUARANTINE = 'quarantine'
DMARC_SKIP = 'skip'
DMARC_UNSIGNED = 'unsigned'
DMARC_PASS = 'pass'
DMARC_FAIL = 'fail'
DMARC_RECORDFAIL = 'recordfail'



def extract_from_domains(suspect, header='From', get_display_part=False):
    """
    Returns a list of all domains found in From header
    :param suspect: Suspect
    :param header: name of header to extract, defaults to From
    :param get_display_part: set to True to search and extract domains found in display part, not the actual addresses
    :return: list of domain names or None in case of errors
    """

    # checking display part there's no need checking for the validity of the associated
    # mail address
    from_addresses = suspect.parse_from_type_header(header=header, validate_mail=(not get_display_part))
    if len(from_addresses) < 1:
        return None
    
    from_doms = []
    for item in from_addresses:
        if get_display_part:
            domain_match = re.search("(?<=@)[\w.-]+", item[0])
            if domain_match is None:
                continue
            from_doms.append(domain_match.group())
        else:
            try:
                from_doms.append(extract_domain(item[1]))
            except Exception as e:
                logging.getLogger("fuglu.extract_from_domains").exception(e)

    from_addrs = list(set(from_doms))
    return from_addrs



def extract_from_domain(suspect, header='From', get_display_part=False):
    """
    Returns the most significant domain found in From header.
    Usually this means the last domain that can be found.
    :param suspect: Suspect object
    :param header: name of header to extract, defaults to From
    :param get_display_part: set to True to search and extract domains found in display part, not the actual addresses
    :return: string with domain name or None if nothing found
    """
    from_doms = extract_from_domains(suspect, header, get_display_part)
    if from_doms:
        from_doms = from_doms[-1]
    else:
        from_doms = None
    return from_doms



class ARCVerifyPlugin(ScannerPlugin):
    """
    This plugin checks the ARC signature of the message and sets tags.
    """
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
    
    
    def __str__(self):
        return "ARC Verify"


    def examine(self, suspect):
        if not DKIMPY_AVAILABLE:
            suspect.debug("dkimpy not available, can not check")
            suspect.set_tag('ARCVerify.skipreason', 'dkimpy library not available')
            return DUNNO
        
        msgrep = suspect.get_message_rep()
        for hdrname in ARC.ARC_HEADERS:
            hdrname = force_uString(hdrname)
            if hdrname not in msgrep:
                suspect.set_tag('ARCVerify.skipreason', 'not ARC signed')
                suspect.write_sa_temp_header(ARC_SAHEADER, DKIM_UNSIGNED)
                suspect.debug("ARC signature header %s not found" % hdrname)
                return DUNNO
    
        source = suspect.get_original_source()
        try:
            # use the local logger of the plugin but prepend the fuglu id
            d = ARC(source, logger=PrependLoggerMsg(self.logger, prepend=suspect.id, maxlevel=logging.INFO))
            try:
                valid = d.verify()
                self.logger.debug("%s: ARC validity %s" % (suspect.id, valid))
            except Exception as de:
                self.logger.warning("%s: ARC validation failed: %s" % (suspect.id, str(de)))
                valid = False
            suspect.set_tag("ARCVerify.sigvalid", valid)
            suspect.write_sa_temp_header(ARC_SAHEADER, DKIM_VALID if valid else DKIM_INVALID)
        except MessageFormatError as e:
            self.logger.warning("%s: ARC validation failed: Message format error" % suspect.id)
            self.logger.debug("%s: %s" % (suspect.id, str(e)))
            suspect.set_tag('ARCVerify.skipreason', 'plugin error')
        except NameError as e:
            self.logger.warning("%s: ARC validation failed due to missing dependency: %s" % (suspect.id, str(e)))
            suspect.set_tag('ARCVerify.skipreason', 'plugin error')
        except Exception as e:
            self.logger.warning("%s: ARC validation failed: %s" % (suspect.id, str(e)))
            suspect.set_tag('ARCVerify.skipreason', 'plugin error')
    
        return DUNNO


    def lint(self):
        all_ok = self.check_config()
    
        if not DKIMPY_AVAILABLE:
            print("Missing dependency: dkimpy https://launchpad.net/dkimpy")
            all_ok = False
    
        if not DNSQUERY_EXTENSION_ENABLED:
            print("Missing dependency: no supported DNS libary found: pydns or dnspython")
            all_ok = False
    
        return all_ok



class DKIMVerifyPlugin(ScannerPlugin):
    """
This plugin checks the DKIM signature of the message and sets tags...
DKIMVerify.sigvalid : True if there was a valid DKIM signature, False if there was an invalid DKIM signature
the tag is not set if there was no dkim header at all

DKIMVerify.skipreason: set if the verification has been skipped

The plugin does not take any action based on the DKIM test result since a failed DKIM validation by itself
should not cause a message to be treated any differently. Other plugins might use the DKIM result
in combination with other factors to take action (for example a "DMARC" plugin could use this information)

It is currently recommended to leave both header and body canonicalization as 'relaxed'. Using 'simple' can cause the signature to fail.
    """
    
    # set as class variable for simple unit test monkey patching
    DKIM = DKIM
    
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        self.skiplist = FileList(filename=None, strip=True, skip_empty=True, skip_comments=True, lowercase=True)
        self.requiredvars = {
            'skiplist': {
                'default': '',
                'description': 'File containing a list of domains (one per line) which are not checked'
            },
        }
    
    
    def __str__(self):
        return "DKIM Verify"
    
    
    def examine(self, suspect):
        if not DKIMPY_AVAILABLE:
            suspect.debug("dkimpy not available, can not check")
            suspect.set_tag('DKIMVerify.skipreason', 'dkimpy library not available')
            return DUNNO
        
        hdr_from_domain = extract_from_domain(suspect)
        if not hdr_from_domain:
            self.logger.debug('%s DKIM Verification skipped, no header from address')
            suspect.set_tag("DKIMVerify.skipreason", 'no header from address')
            return DUNNO
            
        self.skiplist.filename = self.config.get(self.section, 'skiplist')
        skiplist = self.skiplist.get_list()
        if hdr_from_domain in skiplist:
            self.logger.debug('%s DKIM Verification skipped, sender domain skiplisted')
            suspect.set_tag("DKIMVerify.skipreason", 'sender domain skiplisted')
            return DUNNO
        
        dkimhdrs = suspect.get_message_rep().get_all('dkim-signature')
        if not dkimhdrs:
            suspect.set_tag('DKIMVerify.skipreason', 'not dkim signed')
            suspect.write_sa_temp_header(DKIM_SAHEADER, DKIM_UNSIGNED)
            suspect.debug("No dkim signature header found")
            return DUNNO
        
        source = suspect.get_original_source()
        try:
            # use the local logger of the plugin but prepend the fuglu id
            d = self.DKIM(source, logger=PrependLoggerMsg(self.logger, prepend=suspect.id, maxlevel=logging.INFO))
            valid = False
            authordomain = False
            senderdomain = False
            saval = DKIM_INVALID
            try:
                # one dkim header has to be valid
                for i in range(0, len(dkimhdrs)):
                    valid = d.verify(idx=i)
                    if valid:
                        # wants bytes, returns dict of bytes
                        tags = dkimutil.parse_tag_value(force_bString(dkimhdrs[i]))
                        if tags.get(b'd') == force_bString(hdr_from_domain) or tags.get(b'd', b'').endswith(force_bString(f'.{hdr_from_domain}')):
                            authordomain = True
                            saval = DKIM_VALID_AUTHOR
                        elif not authordomain and suspect.from_domain and (tags.get(b'd') == force_bString(suspect.from_domain) or tags.get(b'd', b'').endswith(force_bString(f'.{suspect.from_domain}'))):
                            senderdomain = True
                            saval = DKIM_VALID_SENDER
                        elif not authordomain and not senderdomain:
                            saval = DKIM_VALID
                    self.logger.debug("%s: DKIM idx=%s valid=%s authordomain=%s senderdomain=%s" % (suspect.id, i, valid, authordomain, senderdomain))
            except DKIMException as de:
                self.logger.warning("%s: DKIM validation failed: %s" % (suspect.id, str(de)))
            
            suspect.set_tag("DKIMVerify.sigvalid", valid)
            suspect.set_tag("DKIMVerify.result", saval)
            suspect.set_tag("DKIMVerify.sigvalidauthor", authordomain)
            suspect.set_tag("DKIMVerify.sigvalidsender", senderdomain)
            suspect.write_sa_temp_header(DKIM_SAHEADER, saval)
        except MessageFormatError as e:
            self.logger.warning("%s: DKIM validation failed: Message format error" % suspect.id)
            self.logger.debug("%s: %s" % (suspect.id, str(e)))
            suspect.set_tag('DKIMVerify.skipreason', 'plugin error')
        except NameError as e:
            self.logger.warning("%s: DKIM validation failed due to missing dependency: %s" % (suspect.id, str(e)))
            suspect.set_tag('DKIMVerify.skipreason', 'plugin error')
        except Exception as e:
            self.logger.warning("%s: DKIM validation failed: %s" % (suspect.id, str(e)))
            suspect.set_tag('DKIMVerify.skipreason', 'plugin error')
            
        return DUNNO
    
    
    def lint(self):
        all_ok = self.check_config()
        
        if not DKIMPY_AVAILABLE:
            print("Missing dependency: dkimpy https://launchpad.net/dkimpy")
            all_ok = False
            
        if not DNSQUERY_EXTENSION_ENABLED:
            print("Missing dependency: no supported DNS libary found: pydns or dnspython")
            all_ok = False
        
        return all_ok

# test:
# plugdummy.py -p ...  domainauth.DKIMSignPlugin -s <sender> -o canonicalizeheaders:relaxed -o canonicalizebody:simple -o signbodylength:False
# cat /tmp/fuglu_dummy_message_out.eml | swaks -f <sender>  -s <server>
# -au <username> -ap <password> -4 -p 587 -tls -d -  -t
# <someuser>@gmail.com


class DKIMSignPlugin(ScannerPlugin):

    """
Add DKIM Signature to outgoing mails

Setting up your keys:

::

    mkdir -p /etc/fuglu/dkim
    domain=example.com
    openssl genrsa -out /etc/fuglu/dkim/${domain}.key 1024
    openssl rsa -in /etc/fuglu/dkim/${domain}.key -out /etc/fuglu/dkim/${domain}.pub -pubout -outform PEM
    # print out the DNS record:
    echo -n "default._domainkey TXT  \\"v=DKIM1; k=rsa; p=" ; cat /etc/fuglu/dkim/${domain}.pub | grep -v 'PUBLIC KEY' | tr -d '\\n' ; echo ";\\""


If fuglu handles both incoming and outgoing mails you should make sure that this plugin is skipped for incoming mails

    """

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        self.requiredvars = {
            'privatekeyfile': {
                'description': "Location of the private key file. supports standard template variables plus additional ${header_from_domain} which extracts the domain name from the From: -Header",
                'default': "/etc/fuglu/dkim/${header_from_domain}.key",
            },
            
            'canonicalizeheaders': {
                'description': "Type of header canonicalization (simple or relaxed)",
                'default': "relaxed",
            },
            
            'canonicalizebody': {
                'description': "Type of body canonicalization (simple or relaxed)",
                'default': "relaxed",
            },
            
            'selector': {
                'description': 'selector to use when signing, supports templates',
                'default': 'default',
            },
            
            'signheaders': {
                'description': 'comma separated list of headers to sign. empty string=sign all headers',
                'default': 'From,Reply-To,Subject,Date,To,CC,Resent-Date,Resent-From,Resent-To,Resent-CC,In-Reply-To,References,List-Id,List-Help,List-Unsubscribe,List-Subscribe,List-Post,List-Owner,List-Archive',
            },
            
            'signbodylength': {
                'description': 'include l= tag in dkim header',
                'default': 'False',
            },
        }


    def __str__(self):
        return "DKIM Sign"


    def examine(self, suspect):
        if not DKIMPY_AVAILABLE:
            suspect.debug("dkimpy not available, can not check")
            self.logger.error("DKIM signing skipped - missing dkimpy library")
            return DUNNO
        
        message = suspect.get_source()
        domain = extract_from_domain(suspect)
        addvalues = dict(header_from_domain=domain)
        selector = apply_template(self.config.get(self.section, 'selector'), suspect, addvalues)
        
        if domain is None:
            self.logger.debug("%s: Failed to extract From-header domain for DKIM signing" % suspect.id)
            return DUNNO
        
        privkeyfile = apply_template(self.config.get(self.section, 'privatekeyfile'), suspect, addvalues)
        if not os.path.isfile(privkeyfile):
            self.logger.debug("%s: DKIM signing failed for domain %s, private key not found: %s" % (suspect.id, domain, privkeyfile))
            return DUNNO
        
        with open(privkeyfile, 'br') as f:
            privkeycontent = f.read()
        
        canH = Simple
        canB = Simple
        
        if self.config.get(self.section, 'canonicalizeheaders').lower() == 'relaxed':
            canH = Relaxed
        if self.config.get(self.section, 'canonicalizebody').lower() == 'relaxed':
            canB = Relaxed
        canon = (canH, canB)
        headerconfig = self.config.get(self.section, 'signheaders')
        if headerconfig is None or headerconfig.strip() == '':
            inc_headers = None
        else:
            inc_headers = headerconfig.strip().split(',')
        
        blength = self.config.getboolean(self.section, 'signbodylength')
        
        dkimhdr = sign(message, force_bString(selector), force_bString(domain), privkeycontent,
                       canonicalize=canon, include_headers=inc_headers, length=blength, logger=suspect.get_tag('debugfile'))
        if dkimhdr.startswith(b'DKIM-Signature: '):
            dkimhdr = dkimhdr[16:]

        suspect.addheader('DKIM-Signature', dkimhdr, immediate=True)


    def lint(self):
        all_ok = self.check_config()
        
        if not DKIMPY_AVAILABLE:
            print("Missing dependency: dkimpy https://launchpad.net/dkimpy")
            all_ok = False
        if not DNSQUERY_EXTENSION_ENABLED:
            print("Missing dependency: no supported DNS libary found. pydns or dnspython")
            all_ok = False

        # if privkey is a filename (no placeholders) check if it exists
        privkeytemplate = self.config.get(self.section, 'privatekeyfile')
        if '{' not in privkeytemplate and not os.path.exists(privkeytemplate):
            print("Private key file %s not found" % privkeytemplate)
            all_ok = False

        return all_ok


class SPFPlugin(ScannerPlugin):

    """
This plugin checks the SPF status and sets tag 'SPF.status' to one of the official states 'pass', 'fail', 'neutral',
'softfail, 'permerror', 'temperror' or 'skipped' if the SPF check could not be peformed.
Tag 'SPF.explanation' contains a human readable explanation of the result.
Additionally information to be used by SA plugin is added

The plugin does not take any action based on the SPF test result since. Other plugins might use the SPF result
in combination with other factors to take action (for example a "DMARC" plugin could use this information)
    """
    
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        self.skiplist = FileList(filename=None, strip=True, skip_empty=True, skip_comments=True, lowercase=True)
        self.requiredvars = {
            'max_lookups': {
                'default': '10',
                'description': 'maximum number of lookups (RFC defaults to 10)',
            },
            'skiplist': {
                'default': '',
                'description': 'File containing a list of domains (one per line) which are not checked'
            },
            'temperror_retries': {
                'default': '3',
                'description': 'maximum number of retries on temp error',
            },
            'temperror_sleep': {
                'default': '3',
                'description': 'waiting interval between retries on temp error',
            },
            'on_fail': {
                'default': 'DUNNO',
                'description': 'Action for SPF fail. Set to DUNNO if running in after-queue mode.',
            },
            'on_softfail': {
                'default': 'DUNNO',
                'description': 'Action for SPF softfail. Set to DUNNO if running in after-queue mode.',
            },
            'messagetemplate': {
                'default': 'SPF ${result} for domain ${from_domain} from ${client_address} : ${explanation}',
                'description': 'reject message template for policy violators'
            },
        }
    
    
    def __str__(self):
        return "SPF Check"
    
    
    def _spf_lookup(self, ip, from_address, helo, retries=3):
        spf.MAX_LOOKUP = self.config.getint(self.section, 'max_lookups')
        result, explanation = spf.check2(ip, from_address, helo)
        if result == 'temperror' and retries>0:
            time.sleep(self.config.getint(self.section, 'temperror_sleep'))
            retries -= 1
            result, explanation = self._spf_lookup(ip, from_address, helo, retries)
        return result, explanation
    
    
    def _get_clientinfo(self, suspect):
        clientinfo = suspect.get_client_info(self.config)
        if clientinfo is None:
            suspect.debug("client info not available for SPF check")
            self.logger.warning("%s: SPF Check skipped, could not get client info" % suspect.id)
            suspect.set_tag('SPF.status', 'skipped')
            suspect.set_tag("SPF.explanation", 'could not extract client information')
            return None, None
        helo, ip, revdns = clientinfo
        return ip, helo
    
    
    def examine(self, suspect):
        action = DUNNO
        if not PYSPF_AVAILABLE:
            suspect.debug("pyspf not available, can not check")
            self.logger.warning("%s: SPF Check skipped, pyspf unavailable" % suspect.id)
            suspect.set_tag('SPF.status', 'skipped')
            suspect.set_tag("SPF.explanation", 'missing dependency')
            return action
        
        if not suspect.from_address:
            self.logger.debug('%s SPF Check skipped, bounce')
            suspect.set_tag('SPF.status', 'skipped')
            suspect.set_tag("SPF.explanation", 'skipped bounce')
            return action
        
        self.skiplist.filename = self.config.get(self.section, 'skiplist')
        checkdomains = self.skiplist.get_list()
        if suspect.from_domain in checkdomains:
            self.logger.debug('%s SPF Check skipped, sender domain skiplisted')
            suspect.set_tag('SPF.status', 'skipped')
            suspect.set_tag("SPF.explanation", 'sender domain skiplisted')
            return action
        
        ip, helo = self._get_clientinfo(suspect)
        if ip is None:
            return action
        
        message = None
        retries = self.config.getint(self.section, 'temperror_retries')
        try:
            result, explanation = self._spf_lookup(ip, suspect.from_address, helo, retries)
            suspect.set_tag("SPF.status", result)
            suspect.set_tag("SPF.explanation", explanation)
            suspect.write_sa_temp_header('X-SPFCheck', result)
            suspect.debug("SPF status: %s (%s)" % (result, explanation))
            message = apply_template(self.config.get(self.section, 'messagetemplate'), suspect, dict(result=result, explanation=explanation))
            if result == 'fail':
                action = string_to_actioncode(self.config.get(self.section, 'on_fail'))
            elif result == 'softfail':
                action = string_to_actioncode(self.config.get(self.section, 'on_softfail'))
        except Exception as e:
            suspect.set_tag('SPF.status', 'skipped')
            suspect.set_tag("SPF.explanation", str(e))
            self.logger.warning('%s SPF check failed for %s due to %s' % (suspect.id, suspect.from_domain, str(e)))
            
        return action, message
    
    
    def lint(self):
        all_ok = self.check_config()
        
        if not PYSPF_AVAILABLE:
            print("Missing dependency: pyspf")
            all_ok = False
            
        if not DNSQUERY_EXTENSION_ENABLED:
            print("Missing dependency: no supported DNS libary found: pydns or dnspython")
            all_ok = False
            
        return all_ok


class DMARCPlugin(ScannerPlugin):
    """
    **EXPERIMENTAL**
    This plugin evaluates DMARC policy of the sender domain.
    
    This plugin depends on tags written by SPFPlugin and DKIMVerifyPlugin, so they must run beforehand.
    """
    
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        if DOMAINMAGIC_AVAILABLE:
            self.tldmagic = TLDMagic()
        else:
            self.tldmagic = None
        
        self.requiredvars = {
            'on_reject': {
                'default': 'DUNNO',
                'description': 'Action if DMARC disposition evaluates to "reject". Set to DUNNO if running in after-queue mode.',
            },
            'messagetemplate': {
                'default': 'DMARC diposition of ${header_from_domain} recommends rejection',
                'description': 'reject message template for policy violators'
            },
        }
    
    
    def _query_dmarc(self, domain):
        if self.tldmagic is not None:
            domain = self.tldmagic.get_domain(domain)
        
        hostname = '_dmarc.%s' % domain
        result = lookup(hostname, QTYPE_TXT)
        if result is None:
            return None
        
        for item in result:
            item = item.strip('"')
            if item.lower().startswith('v=dmarc1'):
                record = item
                break # TODO: handle multiple dmarc records
        else:
            record = None
        
        return record
    
    
    def _get_dkim_result(self, suspect):
        for line in suspect.get_sa_temp_headers().splitlines():
            hdr, value = force_uString(line).split(':', 1)
            if hdr == DKIM_SAHEADER:
                value = value.strip()
                break
        else:
            value = None
        
        # unsigned should return None
        dkim_value_map = {
            DKIM_VALID: dmarc.DKIM_PASS,
            DKIM_INVALID: dmarc.DKIM_FAIL,
        }
        dkim_result = dkim_value_map.get(value)
        self.logger.debug('%s dkim result=%s status=%s' % (suspect.id, dkim_result, value))
        return dkim_result
    
    
    def _parse_dkim_list(self, header):
        tags = {}
        error = False
        tag_specs = header.strip().split(';')
        # Trailing semicolons are valid.
        if not tag_specs[-1]:
            tag_specs.pop()
        for tag_spec in tag_specs:
            try:
                key, value = [x.strip() for x in tag_spec.split('=', 1)]
            except ValueError:
                error = True
                break
            if re.match(r'^[a-zA-Z](\w)*', key) is None:
                error = True
                break
            if key in tags:
                error = True
                break
            tags[key] = value
        if error:
            tags = {}
        return tags
    
    
    def _get_dkim_domain_selector(self, suspect):
        msgrep = suspect.get_message_rep()
        dkimheader = msgrep.get('dkim-signature')
        dkimheader = Suspect.decode_msg_header(dkimheader)
        tags = self._parse_dkim_list(dkimheader)
        domain = tags.get('d')
        selector = tags.get('s')
        self.logger.debug('%s extracted dkim domain=%s selector=%s from dkim header length=%s with tag count=%s' % (suspect.id, domain, selector, len(dkimheader), len(tags)))
        return domain, selector
    
    
    def _get_spf_result(self, suspect):
        status = suspect.get_tag('SPF.status', 'unknown')
        
        # skipped, unkonwn, none should return None
        spf_value_map = {
            'pass': dmarc.SPF_PASS,
            'softfail': dmarc.SPF_FAIL,
            'fail': dmarc.SPF_FAIL,
            'neutral': dmarc.SPF_NEUTRAL,
            'temperror': dmarc.SPF_TEMPFAIL,
            'permfail': dmarc.SPF_PERMFAIL,
        }
        spf_result = spf_value_map.get(status)
        self.logger.debug('%s spf result=%s status=%s' % (suspect.id, spf_result, status))
        return spf_result
    
    
    def _mk_aspf(self, from_domain, spf_result):
        if spf_result is None:
            aspf = None
        else:
            aspf = dmarc.SPF(domain=from_domain, result=spf_result)
        return aspf
    
    
    def _mk_adkim(self, dkim_domain, dkim_result, dkim_selector):
        if dkim_result is None:
            adkim = None
        else:
            adkim = dmarc.DKIM(domain=dkim_domain, result=dkim_result, selector=dkim_selector)
        return adkim
    
    
    def _do_dmarc_check(self, dmarc_record, header_from_domain, aspf, adkim, suspectid):
        result = None
        dispo = None
        try:
            d = dmarc.DMARC()
            p = d.parse_record(record=dmarc_record, domain=header_from_domain)
            r = d.get_result(p, spf=aspf, dkim=adkim)
            result = r.result
            dispo = r.disposition
        except dmarc.RecordSyntaxError as e:
            self.logger.info('%s invalid DMARC record: %s' % (suspectid, str(e)))
        except ValueError as e:
            if aspf is not None:
                dbgaspf = '%s;%s' % (aspf.domain, aspf.result)
            else:
                dbgaspf = 'none'
            if adkim is not None:
                dbgadkim = '%s;%s;%s' % (adkim.domain, adkim.result, adkim.selector)
            else:
                dbgadkim = None
            self.logger.error('%s DMARC ValueError: header_from_domain=%s aspf=%s adkim=%s dmarc_record=%s' % (suspectid, header_from_domain, dbgaspf, dbgadkim, dmarc_record))
        return result, dispo
    
    
    def examine(self, suspect):
        if not DMARC_AVAILABLE:
            self.logger.debug('%s DMARC check skipped' % suspect.id)
            return DUNNO
        
        header_from_domain = extract_from_domain(suspect)
        if not header_from_domain:
            suspect.write_sa_temp_header(DMARC_SAHEADER_RESULT, DMARC_SKIP)
            self.logger.debug('%s no valid domain found in From header' % suspect.id)
            return DUNNO
        
        dmarc_record = self._query_dmarc(header_from_domain)
        if dmarc_record is None:
            suspect.write_sa_temp_header(DMARC_SAHEADER_RESULT, DMARC_UNSIGNED)
            self.logger.debug('%s no DMARC record found' % suspect.id)
            return DUNNO
        
        spf_result = self._get_spf_result(suspect)
        dkim_result = self._get_dkim_result(suspect)
        if dkim_result is None:
            self.logger.debug('%s not extracting dkim data from header due to dkim_result=%s' % (suspect.id, dkim_result))
            dkim_domain = dkim_selector = None
        else:
            dkim_domain, dkim_selector = self._get_dkim_domain_selector(suspect)
        
        aspf = self._mk_aspf(suspect.from_domain, spf_result)
        adkim = self._mk_adkim(dkim_domain, dkim_result, dkim_selector)
        result, dispo = self._do_dmarc_check(dmarc_record, header_from_domain, aspf, adkim, suspect.id)
        
        if result is None:
            suspect.write_sa_temp_header(DMARC_SAHEADER_RESULT, DMARC_RECORDFAIL)
        elif result == dmarc.POLICY_PASS:
            suspect.write_sa_temp_header(DMARC_SAHEADER_RESULT, DMARC_PASS)
        elif result == dmarc.POLICY_FAIL:
            suspect.write_sa_temp_header(DMARC_SAHEADER_RESULT, DMARC_FAIL)
        
        action = DUNNO
        message = None
        if dispo == dmarc.POLICY_DIS_REJECT:
            action = string_to_actioncode(self.config.get(self.section, 'on_reject'))
            message = apply_template(self.config.get(self.section, 'messagetemplate'), suspect, dict(header_from_domain=header_from_domain))
            suspect.write_sa_temp_header(DMARC_SAHEADER_DISPO, DMARC_REJECT)
        elif dispo == dmarc.POLICY_DIS_QUARANTINE:
            suspect.write_sa_temp_header(DMARC_SAHEADER_DISPO, DMARC_QUARANTINE)
        
        return action, message
        
        
    def __str__(self):
        return "DMARC"
    
    
    def lint(self):
        all_ok = self.check_config()
        
        if not DMARC_AVAILABLE:
            print("Missing dependency: dmarc")
            all_ok = False
        
        if not DNSQUERY_EXTENSION_ENABLED:
            print("Missing dependency: no supported DNS libary found: pydns or dnspython")
            all_ok = False
        
        return all_ok


class DomainAuthPlugin(ScannerPlugin):

    """
    **EXPERIMENTAL**
    This plugin checks the header from domain against a list of domains which must be authenticated by DKIM and/or SPF.
    This is somewhat similar to DMARC but instead of asking the sender domain for a DMARC policy record this plugin allows you to force authentication on the recipient side.
    
    This plugin depends on tags written by SPFPlugin and DKIMVerifyPlugin, so they must run beforehand.
    """

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.requiredvars = {
            'domainsfile': {
                'description': "File containing a list of domains (one per line) which must be DKIM and/or SPF authenticated",
                'default': "/etc/fuglu/auth_required_domains.txt",
            },
            'failaction': {
                'default': 'DUNNO',
                'description': "action if the message doesn't pass authentication (DUNNO, REJECT)",
            },

            'rejectmessage': {
                'default': 'sender domain ${header_from_domain} must pass DKIM and/or SPF authentication',
                'description': "reject message template if running in pre-queue mode",
            },
        }
        self.logger = self._logger()
        self.filelist = FileList(filename=None, strip=True, skip_empty=True, skip_comments=True, lowercase=True)
    
    
    def examine(self, suspect):
        self.filelist.filename = self.config.get(self.section, 'domainsfile')
        checkdomains = self.filelist.get_list()

        envelope_sender_domain = suspect.from_domain.lower()
        header_from_domain = extract_from_domain(suspect)
        if header_from_domain is None:
            return

        if header_from_domain not in checkdomains:
            return

        # TODO: do we need a tag from dkim to check if the verified dkim domain
        # actually matches the header from domain?
        dkimresult = suspect.get_tag('DKIMVerify.sigvalid', False)
        if dkimresult is True:
            return DUNNO

        # DKIM failed, check SPF if envelope senderdomain belongs to header
        # from domain
        spfresult = suspect.get_tag('SPF.status', 'unknown')
        if (envelope_sender_domain == header_from_domain or envelope_sender_domain.endswith('.%s' % header_from_domain)) and spfresult == 'pass':
            return DUNNO

        failaction = self.config.get(self.section, 'failaction')
        actioncode = string_to_actioncode(failaction, self.config)

        values = dict(header_from_domain=header_from_domain)
        message = apply_template(self.config.get(self.section, 'rejectmessage'), suspect, values)
        return actioncode, message
    
    
    def flag_as_spam(self, suspect):
        suspect.tags['spam']['domainauth'] = True
    
    
    def __str__(self):
        return "DomainAuth"
    
    
    def lint(self):
        allok = self.check_config() and self.lint_file()
        return allok
    
    
    def lint_file(self):
        filename = self.config.get(self.section, 'domainsfile')
        if not os.path.exists(filename):
            print("domains file %s not found" % filename)
            return False
        return True


class SpearPhishPlugin(ScannerPlugin):
    """Mark spear phishing mails as virus

    The spearphish plugin checks if the sender domain in the "From"-Header matches the envelope recipient Domain ("Mail
    from my own domain") but the message uses a different envelope sender domain. This blocks many spearphish attempts.

    Note that this plugin can cause blocks of legitimate mail , for example if the recipient domain is using a third party service
    to send newsletters in their name. Such services often set the customers domain in the from headers but use their own domains in the envelope for
    bounce processing. Use the 'Plugin Skipper' or any other form of whitelisting in such cases.
    """

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section=section)
        self.logger = self._logger()
        self.filelist = FileList(strip=True, skip_empty=True, skip_comments=True, lowercase=True,
                                 additional_filters=None, minimum_time_between_reloads=30)

        self.requiredvars = {
            'domainsfile': {
                'default': '/etc/fuglu/spearphish-domains',
                'description': 'Filename where we load spearphish domains from. One domain per line. If this setting is empty, the check will be applied to all domains.',
            },
            'virusenginename': {
                'default': 'Fuglu SpearPhishing Protection',
                'description': 'Name of this plugins av engine',
            },
            'virusname': {
                'default': 'TRAIT.SPEARPHISH',
                'description': 'Name to use as virus signature',
            },
            'virusaction': {
                'default': 'DEFAULTVIRUSACTION',
                'description': "action if spear phishing attempt is detected (DUNNO, REJECT, DELETE)",
            },
            'rejectmessage': {
                'default': 'threat detected: ${virusname}',
                'description': "reject message template if running in pre-queue mode and virusaction=REJECT",
            },
            'dbconnection':{
                'default':"mysql://root@localhost/spfcheck?charset=utf8",
                'description':'SQLAlchemy Connection string. Leave empty to disable SQL lookups',
            },
            'domain_sql_query':{
                'default':"SELECT check_spearphish from domain where domain_name=:domain",
                'description':'get from sql database :domain will be replaced with the actual domain name. must return boolean field check_spearphish',
            },
            'check_display_part': {
                'default': 'False',
                'description': "set to True to also check display part of From header (else email part only)",
            },
            'checkbounces': {
                'default': 'True',
                'description': 'disable this if you want to exclude mail with empty envelope sender (bounces, NDRs, OOO) from being marked as spearphish'
            },
        }


    def get_domain_setting(self, domain, dbconnection, sqlquery, cache, cachename, default_value=None, logger=None):
        if logger is None:
            logger = logging.getLogger()
        
        cachekey = '%s-%s' % (cachename, domain)
        cached = cache.get_cache(cachekey)
        if cached is not None:
            logger.debug("got cached setting for %s" % domain)
            return cached
    
        settings = default_value
    
        try:
            session = get_session(dbconnection)
    
            # get domain settings
            dom = session.execute(sqlquery, {'domain': domain}).fetchall()
    
            if not dom and not dom[0] and len(dom[0]) == 0:
                logger.warning(
                    "Can not load domain setting - domain %s not found. Using default settings." % domain)
            else:
                settings = dom[0][0]
    
            session.close()
    
        except Exception as e:
            logger.error("Exception while loading setting for %s : %s" % (domain, str(e)))
    
        cache.put_cache(cachekey, settings)
        logger.debug("refreshed setting for %s" % domain)
        return settings
    
    
    def should_we_check_this_domain(self,suspect):
        domainsfile = self.config.get(self.section, 'domainsfile')
        if domainsfile.strip()=='': # empty config -> check all domains
            return True

        if not os.path.exists(domainsfile):
            return False

        self.filelist.filename = domainsfile
        envelope_recipient_domain = suspect.to_domain.lower()
        checkdomains = self.filelist.get_list()
        if envelope_recipient_domain in checkdomains:
            return True
        
        dbconnection = self.config.get(self.section, 'dbconnection').strip()
        sqlquery = self.config.get(self.section,'domain_sql_query')
        do_check = False
        if dbconnection != '':
            cache = get_default_cache()
            cachename = self.section
            do_check = self.get_domain_setting(suspect.to_domain, dbconnection, sqlquery, cache, cachename, False, self.logger)
        return do_check
    
    
    def examine(self, suspect):
        if not self.should_we_check_this_domain(suspect):
            return DUNNO
        envelope_recipient_domain = suspect.to_domain.lower()
        envelope_sender_domain = suspect.from_domain.lower()
        if envelope_sender_domain == envelope_recipient_domain or envelope_sender_domain.endswith(f'.{envelope_recipient_domain}'):
            return DUNNO  # we only check the message if the env_sender_domain differs. If it's the same it will be caught by other means (like SPF)
        
        if not self.config.getboolean(self.section, 'checkbounces') and suspect.from_address=='':
            return DUNNO
        
        header_from_domains = extract_from_domains(suspect)
        if header_from_domains is None:
            header_from_domains = []
        self.logger.debug('%s: checking domain %s (source: From header address part)' % (suspect.id, ','.join(header_from_domains)))
        
        if self.config.getboolean(self.section, 'check_display_part'):
            display_from_domain = extract_from_domain(suspect, get_display_part=True)
            if display_from_domain is not None and display_from_domain not in header_from_domains:
                header_from_domains.append(display_from_domain)
                self.logger.debug('%s: checking domain %s (source: From header display part)' % (suspect.id, display_from_domain))
        
        actioncode = DUNNO
        message = None
        
        for header_from_domain in header_from_domains:
            if header_from_domain == envelope_recipient_domain:
                virusname = self.config.get(self.section, 'virusname')
                virusaction = self.config.get(self.section, 'virusaction')
                actioncode = string_to_actioncode(virusaction, self.config)
                
                logmsg = '%s: spear phish pattern detected, env_rcpt_domain=%s env_sender_domain=%s header_from_domain=%s' % \
                         (suspect.id, envelope_recipient_domain, envelope_sender_domain, header_from_domain)
                self.logger.info(logmsg)
                self.flag_as_phish(suspect, virusname)
                
                message = apply_template(self.config.get(self.section, 'rejectmessage'), suspect, {'virusname': virusname})
                break
        
        return actioncode, message
    
    
    def flag_as_phish(self, suspect, virusname):
        suspect.tags['%s.virus' % self.config.get(self.section, 'virusenginename')] = {'message content': virusname}
        suspect.tags['virus'][self.config.get(self.section, 'virusenginename')] = True
    
    
    def __str__(self):
        return "Spearphish Check"
    
    
    def lint(self):
        allok = self.check_config() and self._lint_file() and self._lint_sql()
        return allok
    
    
    def _lint_file(self):
        filename = self.config.get(self.section, 'domainsfile')
        if not os.path.exists(filename):
            print("Spearphish domains file %s not found" % filename)
            return False
        return True
    
    
    def _lint_sql(self):
        lint_ok = True
        sqlquery = self.config.get(self.section, 'domain_sql_query')
        dbconnection = self.config.get(self.section, 'dbconnection').strip()
        if not SQL_EXTENSION_ENABLED and dbconnection != '':
            print('SQLAlchemy not available, cannot use SQL backend')
            lint_ok = False
        elif dbconnection == '':
            print('No DB connection defined. Disabling SQL backend')
        else:
            if not sqlquery.lower().startswith('select '):
                lint_ok = False
                print('SQL statement must be a SELECT query')
            if lint_ok:
                try:
                    conn = get_session(dbconnection)
                    conn.execute(sqlquery, {'domain': 'example.com'})
                except Exception as e:
                    lint_ok = False
                    print(str(e))
        return lint_ok



class SenderRewriteScheme(ScannerPlugin):
    """
    SRS (Sender Rewriting Scheme) Plugin
    This plugin encrypts envelope sender and decrypts bounce recpient addresses with SRS
    As opposed to postsrsd it decides by RECIPIENT address whether sender address should be rewritten.
    This plugin only works in after queue mode
    
    Required dependencies:
        - pysrs
    Recommended dependencies:
        - sqlalchemy
    """
    
    
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section=section)
        self.logger = self._logger()
        
        self.requiredvars = {
            'dbconnection': {
                'default': "mysql://root@localhost/spfcheck?charset=utf8",
                'description': 'SQLAlchemy Connection string. Leave empty to rewrite all senders',
            },
            
            'domain_sql_query': {
                'default': "SELECT use_srs from domain where domain_name=:domain",
                'description': 'get from sql database :domain will be replaced with the actual domain name. must return field use_srs',
            },
            
            'forward_domain': {
                'default': 'example.com',
                'description': 'the new envelope sender domain',
            },
            
            'secret': {
                'default': '',
                'description': 'cryptographic secret. set the same random value on all your machines',
            },
            
            'maxage': {
                'default': '8',
                'description': 'maximum lifetime of bounces',
            },
            
            'hashlength': {
                'default': '8',
                'description': 'size of auth code',
            },
            
            'separator': {
                'default': '=',
                'description': 'SRS token separator',
            },
            
            'rewrite_header_to': {
                'default': 'True',
                'description': 'set True to rewrite address in To: header in bounce messages (reverse/decrypt mode)',
            },
        }
    
    
    
    def get_sql_setting(self, domain, dbconnection, sqlquery, cache, cachename, default_value=None, logger=None):
        if logger is None:
            logger = logging.getLogger()
        
        cachekey = '%s-%s' % (cachename, domain)
        cached = cache.get_cache(cachekey)
        if cached is not None:
            logger.debug("got cached settings for %s" % domain)
            return cached
        
        settings = default_value
        
        try:
            session = get_session(dbconnection)
            
            # get domain settings
            dom = session.execute(sqlquery, {'domain': domain}).fetchall()
            
            if not dom or not dom[0] or len(dom[0]) == 0:
                logger.debug(
                    "Can not load domain settings - domain %s not found. Using default settings." % domain)
            else:
                settings = dom[0][0]
            
            session.close()
        
        except Exception as e:
            self.logger.error("Exception while loading settings for %s : %s" % (domain, str(e)))
            
            cache.put_cache(cachekey, settings)
        logger.debug("refreshed settings for %s" % domain)
        return settings
    
    
    
    def should_we_rewrite_this_domain(self, suspect):
        forward_domain = self.config.get(self.section, 'forward_domain')
        if suspect.to_domain.lower() == forward_domain:
            return True  # accept for decryption
        
        dbconnection = self.config.get(self.section, 'dbconnection')
        sqlquery = self.config.get(self.section, 'domain_sql_query')
        
        if dbconnection.strip() == '':
            return True  # empty config -> rewrite all domains
        
        cache = get_default_cache()
        cachename = self.section
        setting = self.get_sql_setting(suspect.to_domain, dbconnection, sqlquery, cache, cachename, False, self.logger)
        return setting
    
    
    
    def _init_srs(self):
        secret = self.config.get(self.section, 'secret')
        maxage = self.config.getint(self.section, 'maxage')
        hashlength = self.config.getint(self.section, 'hashlength')
        separator = self.config.get(self.section, 'separator')
        srs = SRS.new(secret=secret, maxage=maxage, hashlength=hashlength, separator=separator, alwaysrewrite=True)
        return srs
    
    
    
    def _update_to_hdr(self, suspect, to_address):
        msgrep = suspect.get_message_rep()
        old_hdr = msgrep.get('To')
        if old_hdr and '<' in old_hdr:
            start = old_hdr.find('<')
            if start < 1:  # malformed header does not contain <> brackets
                start = old_hdr.find(':')  # start >= 0
            name = old_hdr[:start]
            new_hdr = '%s <%s>' % (name, to_address)
        else:
            new_hdr = '<%s>' % to_address
        
        suspect.set_header('To',new_hdr)    
    
    
    def examine(self, suspect):
        if not SRS_AVAILABLE:
            return DUNNO
        
        if not self.should_we_rewrite_this_domain(suspect):
            self.logger.info('SRS: ignoring mail to %s' % suspect.to_address)
            return DUNNO
        
        if not suspect.from_address:
            self.logger.info('SRS: ignoring bounce message')
            return DUNNO
        
        srs = self._init_srs()
        forward_domain = self.config.get(self.section, 'forward_domain').lower()
        if suspect.from_domain.lower() == forward_domain and suspect.from_address.lower().startswith('srs'):
            self.logger.info('SRS %s: skipping already signed address %s' % (suspect.id, suspect.from_address))
        elif suspect.to_domain.lower() == forward_domain and suspect.to_address.lower().startswith('srs'):
            orig_rcpt = suspect.to_address
            try:
                recipient = srs.reverse(orig_rcpt)
                suspect.to_address = recipient
                new_rcpts = [recipient if x == orig_rcpt else x for x in suspect.recipients]
                suspect.recipients = new_rcpts
                if self.config.getboolean(self.section, 'rewrite_header_to'):
                    self._update_to_hdr(suspect, recipient)
                self.logger.info('SRS: decrypted bounce address %s to %s' % (orig_rcpt, recipient))
            except Exception as e:
                self.logger.error('SRS: Failed to decrypt %s reason: %s' % (orig_rcpt, str(e)))
        else:
            orig_sender = suspect.from_address
            try:
                try:
                    sender = srs.forward(orig_sender, forward_domain)
                except AttributeError:
                    # python 3.9 -> deprecated encodestring has been replaced by encodcebytes
                    import base64
                    base64.encodestring = base64.encodebytes
                    sender = srs.forward(orig_sender, forward_domain)
                suspect.from_address = sender
                self.logger.info('SRS: signed %s to %s' % (orig_sender, sender))
            except Exception as e:
                self.logger.error('SRS: Failed to sign %s reason: %s' % (orig_sender, str(e)))
        
        del srs
        return DUNNO
    
    
    def __str__(self):
        return "Sender Rewrite Scheme"
    
    
    def lint(self):
        allok = self.check_config()
        if not SRS_AVAILABLE:
            allok = False
            print('SRS library not found')
        
        if self.config.get(self.section, 'secret') == '':
            allok = False
            print('no secret set in config')
        
        if allok:
            srs = self._init_srs()
            forward_domain = self.config.get(self.section, 'forward_domain')
            try:
                srs.forward('foobar@example.com', forward_domain)
            except AttributeError:
                # python 3.9 -> deprecated encodestring has been replaced by encodcebytes
                import base64
                base64.encodestring = base64.encodebytes
                srs.forward('foobar@example.com', forward_domain)

        sqlquery = self.config.get(self.section, 'domain_sql_query')
        if not sqlquery.lower().startswith('select '):
            allok = False
            print('SQL statement must be a SELECT query')
        if not SQL_EXTENSION_ENABLED:
            allok = False
            print('SQLAlchemy not available, cannot use SQL backend')
        if allok:
            dbconnection = self.config.get(self.section, 'dbconnection')
            if dbconnection.strip() == '':
                print('No DB connection defined. Disabling SQL backend, all addresses will be rewritten.')
            else:
                try:
                    conn = get_session(dbconnection)
                    conn.execute(sqlquery, {'domain': 'example.com'})
                except Exception as e:
                    allok = False
                    print(str(e))
        
        return allok



