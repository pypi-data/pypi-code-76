# -*- coding: utf-8 -*-
#   Copyright 2009-2021 Fumail Project
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
#

"""
A collection of plugins to
- extract URIs/email addresses from mail body and text attachments
- lookup URIs/email addresses on RBLs
These plugins require beautifulsoup and domainmagic
"""

from fuglu.shared import ScannerPlugin, DUNNO, string_to_actioncode, apply_template, FileList, AppenderPlugin, HAVE_BEAUTIFULSOUP, Suspect
from fuglu.stringencode import force_uString
import os
import html
import re
import random
import typing as tp

try:
    from domainmagic.extractor import URIExtractor, fqdn_from_uri, redirect_from_url
    from domainmagic.rbl import RBLLookup
    from domainmagic.tld import TLDMagic
    from domainmagic.mailaddr import domain_from_mail
    DOMAINMAGIC_AVAILABLE = True
except ImportError:
    DOMAINMAGIC_AVAILABLE=False

if HAVE_BEAUTIFULSOUP:
    import bs4 as BeautifulSoup
else:
    BeautifulSoup = None

# remove invisible characters
ichars = r"[\0-\x1F\x7F-\x9F\xAD\u0378\u0379\u037F-\u0383\u038B\u038D\u03A2\u0528-\u0530\u0557\u0558\u0560\u0588\u058B-\u058E\u0590\u05C8-\u05CF\u05EB-\u05EF\u05F5-\u0605\u061C\u061D\u06DD\u070E\u070F\u074B\u074C\u07B2-\u07BF\u07FB-\u07FF\u082E\u082F\u083F\u085C\u085D\u085F-\u089F\u08A1\u08AD-\u08E3\u08FF\u0978\u0980\u0984\u098D\u098E\u0991\u0992\u09A9\u09B1\u09B3-\u09B5\u09BA\u09BB\u09C5\u09C6\u09C9\u09CA\u09CF-\u09D6\u09D8-\u09DB\u09DE\u09E4\u09E5\u09FC-\u0A00\u0A04\u0A0B-\u0A0E\u0A11\u0A12\u0A29\u0A31\u0A34\u0A37\u0A3A\u0A3B\u0A3D\u0A43-\u0A46\u0A49\u0A4A\u0A4E-\u0A50\u0A52-\u0A58\u0A5D\u0A5F-\u0A65\u0A76-\u0A80\u0A84\u0A8E\u0A92\u0AA9\u0AB1\u0AB4\u0ABA\u0ABB\u0AC6\u0ACA\u0ACE\u0ACF\u0AD1-\u0ADF\u0AE4\u0AE5\u0AF2-\u0B00\u0B04\u0B0D\u0B0E\u0B11\u0B12\u0B29\u0B31\u0B34\u0B3A\u0B3B\u0B45\u0B46\u0B49\u0B4A\u0B4E-\u0B55\u0B58-\u0B5B\u0B5E\u0B64\u0B65\u0B78-\u0B81\u0B84\u0B8B-\u0B8D\u0B91\u0B96-\u0B98\u0B9B\u0B9D\u0BA0-\u0BA2\u0BA5-\u0BA7\u0BAB-\u0BAD\u0BBA-\u0BBD\u0BC3-\u0BC5\u0BC9\u0BCE\u0BCF\u0BD1-\u0BD6\u0BD8-\u0BE5\u0BFB-\u0C00\u0C04\u0C0D\u0C11\u0C29\u0C34\u0C3A-\u0C3C\u0C45\u0C49\u0C4E-\u0C54\u0C57\u0C5A-\u0C5F\u0C64\u0C65\u0C70-\u0C77\u0C80\u0C81\u0C84\u0C8D\u0C91\u0CA9\u0CB4\u0CBA\u0CBB\u0CC5\u0CC9\u0CCE-\u0CD4\u0CD7-\u0CDD\u0CDF\u0CE4\u0CE5\u0CF0\u0CF3-\u0D01\u0D04\u0D0D\u0D11\u0D3B\u0D3C\u0D45\u0D49\u0D4F-\u0D56\u0D58-\u0D5F\u0D64\u0D65\u0D76-\u0D78\u0D80\u0D81\u0D84\u0D97-\u0D99\u0DB2\u0DBC\u0DBE\u0DBF\u0DC7-\u0DC9\u0DCB-\u0DCE\u0DD5\u0DD7\u0DE0-\u0DF1\u0DF5-\u0E00\u0E3B-\u0E3E\u0E5C-\u0E80\u0E83\u0E85\u0E86\u0E89\u0E8B\u0E8C\u0E8E-\u0E93\u0E98\u0EA0\u0EA4\u0EA6\u0EA8\u0EA9\u0EAC\u0EBA\u0EBE\u0EBF\u0EC5\u0EC7\u0ECE\u0ECF\u0EDA\u0EDB\u0EE0-\u0EFF\u0F48\u0F6D-\u0F70\u0F98\u0FBD\u0FCD\u0FDB-\u0FFF\u10C6\u10C8-\u10CC\u10CE\u10CF\u1249\u124E\u124F\u1257\u1259\u125E\u125F\u1289\u128E\u128F\u12B1\u12B6\u12B7\u12BF\u12C1\u12C6\u12C7\u12D7\u1311\u1316\u1317\u135B\u135C\u137D-\u137F\u139A-\u139F\u13F5-\u13FF\u169D-\u169F\u16F1-\u16FF\u170D\u1715-\u171F\u1737-\u173F\u1754-\u175F\u176D\u1771\u1774-\u177F\u17DE\u17DF\u17EA-\u17EF\u17FA-\u17FF\u180F\u181A-\u181F\u1878-\u187F\u18AB-\u18AF\u18F6-\u18FF\u191D-\u191F\u192C-\u192F\u193C-\u193F\u1941-\u1943\u196E\u196F\u1975-\u197F\u19AC-\u19AF\u19CA-\u19CF\u19DB-\u19DD\u1A1C\u1A1D\u1A5F\u1A7D\u1A7E\u1A8A-\u1A8F\u1A9A-\u1A9F\u1AAE-\u1AFF\u1B4C-\u1B4F\u1B7D-\u1B7F\u1BF4-\u1BFB\u1C38-\u1C3A\u1C4A-\u1C4C\u1C80-\u1CBF\u1CC8-\u1CCF\u1CF7-\u1CFF\u1DE7-\u1DFB\u1F16\u1F17\u1F1E\u1F1F\u1F46\u1F47\u1F4E\u1F4F\u1F58\u1F5A\u1F5C\u1F5E\u1F7E\u1F7F\u1FB5\u1FC5\u1FD4\u1FD5\u1FDC\u1FF0\u1FF1\u1FF5\u1FFF\u200B-\u200F\u202A-\u202E\u2060-\u206F\u2072\u2073\u208F\u209D-\u209F\u20BB-\u20CF\u20F1-\u20FF\u218A-\u218F\u23F4-\u23FF\u2427-\u243F\u244B-\u245F\u2700\u2B4D-\u2B4F\u2B5A-\u2BFF\u2C2F\u2C5F\u2CF4-\u2CF8\u2D26\u2D28-\u2D2C\u2D2E\u2D2F\u2D68-\u2D6E\u2D71-\u2D7E\u2D97-\u2D9F\u2DA7\u2DAF\u2DB7\u2DBF\u2DC7\u2DCF\u2DD7\u2DDF\u2E3C-\u2E7F\u2E9A\u2EF4-\u2EFF\u2FD6-\u2FEF\u2FFC-\u2FFF\u3040\u3097\u3098\u3100-\u3104\u312E-\u3130\u318F\u31BB-\u31BF\u31E4-\u31EF\u321F\u32FF\u4DB6-\u4DBF\u9FCD-\u9FFF\uA48D-\uA48F\uA4C7-\uA4CF\uA62C-\uA63F\uA698-\uA69E\uA6F8-\uA6FF\uA78F\uA794-\uA79F\uA7AB-\uA7F7\uA82C-\uA82F\uA83A-\uA83F\uA878-\uA87F\uA8C5-\uA8CD\uA8DA-\uA8DF\uA8FC-\uA8FF\uA954-\uA95E\uA97D-\uA97F\uA9CE\uA9DA-\uA9DD\uA9E0-\uA9FF\uAA37-\uAA3F\uAA4E\uAA4F\uAA5A\uAA5B\uAA7C-\uAA7F\uAAC3-\uAADA\uAAF7-\uAB00\uAB07\uAB08\uAB0F\uAB10\uAB17-\uAB1F\uAB27\uAB2F-\uABBF\uABEE\uABEF\uABFA-\uABFF\uD7A4-\uD7AF\uD7C7-\uD7CA\uD7FC-\uF8FF\uFA6E\uFA6F\uFADA-\uFAFF\uFB07-\uFB12\uFB18-\uFB1C\uFB37\uFB3D\uFB3F\uFB42\uFB45\uFBC2-\uFBD2\uFD40-\uFD4F\uFD90\uFD91\uFDC8-\uFDEF\uFDFE\uFDFF\uFE1A-\uFE1F\uFE27-\uFE2F\uFE53\uFE67\uFE6C-\uFE6F\uFE75\uFEFD-\uFF00\uFFBF-\uFFC1\uFFC8\uFFC9\uFFD0\uFFD1\uFFD8\uFFD9\uFFDD-\uFFDF\uFFE7\uFFEF-\uFFFB\uFFFE\uFFFF]"
invisible = re.compile(ichars)


class URIExtract(ScannerPlugin):
    """Extract URIs from message bodies and store them as list in tag body.uris"""
    
    def __init__(self,config,section=None):
        ScannerPlugin.__init__(self,config,section)
        self.logger = self._logger()
        self.extractor=None
                
        self.requiredvars = {
            'domainskiplist':{
                'default':'/etc/fuglu/extract-skip-domains.txt',
                'description':'Domain skip list',
            },
            'maxsize': {
                'default': '10485000',
                'description': 'Maximum size of processed mail parts/attachments.',
            },
            'maxsize_analyse': {
                'default': '2000000',
                'description': 'Maximum size of string to analyze in bytes.',
            },
            'loguris':{
                'default':'no',
                'description':'print extracted uris in fuglu log',
            },
            'usehacks': {
                'default': 'false',
                'description': 'Use extra hacks trying to parse uris',
            },
            'uricheckheaders': {
                'default': '',
                'description': 'List with headers to check for uris',
            },
        }


    def _prepare(self):
        if self.extractor is None:
            self.extractor = URIExtractor()
            skiplist=self.config.get(self.section,'domainskiplist')
            if skiplist!='':
                self.extractor.load_skiplist(skiplist)


    def _run(self,suspect):
        if not DOMAINMAGIC_AVAILABLE:
            self.logger.info('Not scanning - Domainmagic not available')
            return DUNNO

        maxsize = self.config.getint(self.section, 'maxsize')
        maxsize_analyse = self.config.getint(self.section, 'maxsize_analyse')
        usehacks = self.config.getboolean(self.section, 'usehacks')

        self._prepare()
        
        uris = []
        hrefs = []
        for content in self.get_decoded_textparts(suspect, ignore_words_without='.', maxsize=maxsize, maxsize_analyse=maxsize_analyse, hrefs=hrefs,  use_hacks=usehacks):
            try:
                parturis = self.extractor.extracturis(content, use_hacks=usehacks)
                uris.extend(parturis)
            except Exception as e:
                self.logger.error('%s failed to extract URIs from msg part: %s' % (suspect.id, str(e)))
        # add hrefs from html a-tags directly to list
        # - ignore mail addresses (mailto:)
        # - ignore internal references, phone numbers, javascript and html tags (#...)
        # - ignore incomplete template replacements typically starting with square brackets
        hrefs = [h for h in hrefs if not h.lower().startswith(
            ("mailto:", "cid:", "tel:", "fax:", "javascript:", '#', "file:", "[",
             "x-apple-data-detectors:", "applewebdata:",))
                 ]
        uris.extend(hrefs)
        
        subject = suspect.get_message_rep().get("Subject")
        if subject:
            subject = Suspect.decode_msg_header(subject)
        if subject:
            parturis = self.extractor.extracturis(subject, use_hacks=usehacks)
            uris.extend(parturis)
            self.logger.debug(f'{suspect.id} Found URIs in subject part: {parturis}')

        rediruris = self._get_redirected_uris(suspect, uris)
        if rediruris:
            uris.extend(rediruris)
        uris = list(set(uris))  # remove duplicates

        # get uris extracted from headers (stored in headers.uris tag)
        headeruris = self._get_header_uris(suspect=suspect)
        if headeruris:
            self.logger.info(f"{suspect.id} Extracted {len(headeruris)} uris from headers")
            self.logger.debug(f"{suspect.id} Extracted uris \"{headeruris}\" from headers")

        if self.config.getboolean(self.section,'loguris'):
            self.logger.info('%s Extracted URIs: %s' % (suspect.id, uris))
        suspect.set_tag('body.uris', uris)
        return DUNNO
        
    def examine(self, suspect):
        return self._run(suspect)
    
    
    def get_decoded_textparts(self, suspect,bcompatible=True, ignore_words_without=(),
                              maxsize=None, maxsize_analyse=None, hrefs=None, use_hacks=None):
        """bcompatible True will work with FUGLU version before implementation of attachment manager in Suspect """
        textparts = []

        try:
            att_mgr = suspect.att_mgr
        except AttributeError:
            message = 'This version of URIextract is supposed to use a FUGLU version with Attachment Manager. \n' \
                      'Please update your FUGLU version'
            if bcompatible:
                self.logger.warning(message)
            else:
                raise AttributeError(message)
            return self.get_decoded_textparts_deprecated(suspect)

        size_string_analyse = 0
        for attObj in att_mgr.get_objectlist():
            decoded_payload = None
            if attObj.content_fname_check(contenttype_start="text/") \
                    or attObj.content_fname_check(name_end=(".txt", ".html", ".htm")) \
                    or (attObj.defects and attObj.content_fname_check(ctype_start="text/")):
                if maxsize and attObj.filesize and attObj.filesize > maxsize:
                    # ignore parts larger than given limit
                    self.logger.info("%s, ignore part %s with size %s"
                                     % (suspect.id, attObj.filename, attObj.filesize))
                    continue
                decoded_payload = attObj.decoded_buffer_text

                if attObj.content_fname_check(contenttype_contains="html") \
                        or attObj.content_fname_check(name_contains=".htm") \
                        or (attObj.defects and attObj.content_fname_check(ctype_contains="html")):
                    # remove invisible characters (including \r\n) but also check original source
                    decoded_payload_orig = decoded_payload
                    decoded_payload = invisible.sub("", decoded_payload_orig)

                    decoded_payload_replacedchars = ""
                    if use_hacks:
                        # same as above, but handle newlines differently to catch a link starting at a
                        # new line which would otherwise be concatenated and then not recognised by domainmagic
                        decoded_payload_replacedchars = \
                            invisible.sub("", decoded_payload_orig.replace('\r', ' ').replace('\n', ' '))

                    try:
                        decoded_payload = html.unescape(decoded_payload)
                        decoded_payload_replacedchars = html.unescape(decoded_payload_replacedchars)
                    except Exception:
                        self.logger.debug('%s failed to unescape html entities' % suspect.id)

                    if BeautifulSoup:
                        saferedir = []
                        atags = []
                        imgtags = []
                        atagshtml = None
                        if isinstance(hrefs, list):
                            atagshtml = BeautifulSoup.BeautifulSoup(decoded_payload, "lxml").find_all('a')
                            if atagshtml:
                                atags = list(set([atag.get("href") for atag in atagshtml if atag.get("href")]))
                                # some gmail-fu
                                saferedir = list(set([atag.get("data-saferedirecturl") for atag in atagshtml if atag.get("data-saferedirecturl")]))
                                if DOMAINMAGIC_AVAILABLE:
                                    for uri in saferedir[:]:
                                        newuri = redirect_from_url(uri)
                                        if newuri != uri and newuri not in saferedir:
                                            saferedir.append(newuri)
                            # add to hrefs list
                            imgtagshtml = BeautifulSoup.BeautifulSoup(decoded_payload, "lxml").find_all('img')
                            if imgtagshtml:
                                imgtags = list(set([imgtag.get("src") for imgtag in imgtagshtml if imgtag.get("src")]))
                            hrefs.extend(atags)
                            hrefs.extend(saferedir)
                            hrefs.extend(imgtags)
                        suspect.set_tag('uri.safelinks', saferedir)
                        suspect.set_tag('uri.imgsrc', imgtags)

                        # check for a html <base> entity which makes links relative...

                        # basically only the first basetag counts, but here we
                        # extract all in case multiple tags have been inserted to
                        # confuse the algorithm
                        basetags = BeautifulSoup.BeautifulSoup(decoded_payload, "lxml").find_all('base')
                        if basetags and len(basetags) > 1:
                            self.logger.info(f"{suspect.id} found {len(basetags)} <base> tags...")
                        if basetags:
                            basetags = [basetag.get("href") for basetag in basetags if basetag.get("href")]
                        else:
                            basetags = []

                        if basetags:
                            # if there is a base tag with href, extend href's found in a-tags
                            # -> just append result to payload
                            self.logger.info(f"{suspect.id} base tag{'s' if len(basetags) > 1 else ''} found in html!")

                            # check if atags is none and calculste if true
                            # (hrefs for atags might alredy be calculated before)
                            if atagshtml is None:
                                atagshtml = BeautifulSoup.BeautifulSoup(decoded_payload, "lxml").find_all('a')
                                if atagshtml:
                                    atags = list(set([atag.get("href") for atag in atagshtml if atag.get("href")]))
                                else:
                                    atags = []
                            fulllinks = []

                            # combine basetag with atag
                            for basetag in basetags:
                                for atag in atags:
                                    fulllinks.append(basetag + atag)
                            fulllinks.extend(saferedir)
                            fulllinks = list(set(fulllinks))
                            
                            # append links found to payload for further analysis
                            if fulllinks:
                                self.logger.info(f"{suspect.id} <base>-tag: provided {len(fulllinks)} uris for analysis")
                                decoded_payload += " ".join(fulllinks)

                    if decoded_payload_replacedchars:
                        decoded_payload = decoded_payload + " " + decoded_payload_replacedchars

            if attObj.content_fname_check(contenttype="multipart/alternative"):
                if maxsize and len(attObj.decoded_buffer_text) and len(attObj.decoded_buffer_text) > maxsize:
                    # ignore parts larger than given limit
                    self.logger.info("%s, ignore part with contenttype 'multipart/alternative' and size %u"
                                     % (suspect.id, len(attObj.decoded_buffer_text)))
                    continue

                decoded_payload = attObj.decoded_buffer_text

            # Calendar items are special, line continuation starts
            # with a whitespace -> join correctly to detect links correctly
            if attObj.content_fname_check(contenttype="text/calendar"):
                buffer = decoded_payload.replace('\r\n', '\n').split('\n')

                joinedlines = []
                for line in buffer:
                    if line.startswith(' '):
                        if joinedlines:
                            joinedlines[-1] = joinedlines[-1].rstrip() + line.lstrip()
                        else:
                            joinedlines.append(line)
                    else:
                        joinedlines.append(line)
                decoded_payload = " ".join(joinedlines)

            if decoded_payload:
                # Some spam mails create very long lines that will dramatically slow down the regex later on.
                for ignore_element in ignore_words_without:
                    decoded_payload = " ".join([part for part in decoded_payload.split(' ') if ignore_element in part])

                if maxsize_analyse and size_string_analyse + len(decoded_payload) > maxsize_analyse:
                    # ignore parts larger than given limit
                    self.logger.info("%s, ignore part %s due to processed size %u and current size of analyse string %u"
                                     % (suspect.id, attObj.filename, len(decoded_payload), size_string_analyse))
                else:
                    textparts.append(decoded_payload)
                    size_string_analyse += len(decoded_payload)
        return textparts
    
    
    def _get_redirected_uris(self, suspect, uris):
        rediruris = []
        if DOMAINMAGIC_AVAILABLE:
            for uri in uris:
                rediruri = redirect_from_url(uri)
                if rediruri != uri:
                    rediruris.append(rediruri)
            suspect.set_tag('body.uris.redirected', rediruris)
        return rediruris

    def _get_header_uris(self, suspect: Suspect) -> tp.List[str]:
        headerlist = self.config.get(self.section, 'uricheckheaders')
        if not headerlist or not headerlist.strip():
            return []
        headerlist = Suspect.getlist_space_comma_separated(headerlist)
        if not headerlist:
            return []

        ignore_words_without = ["."]
        msgrep = suspect.get_message_rep()

        stringlist2analyse = []
        # loop over given list of header names
        for hname in headerlist:
            # extract headers with given name (multiple possible)
            hobjs = msgrep.get_all(hname)
            if hobjs:
                for h in hobjs:
                    hstring = Suspect.decode_msg_header(h)

                    decoded_payload = ""
                    for ignore_element in ignore_words_without:
                        decoded_payload = " ".join([part for part in hstring.split(' ') if ignore_element in part])

                    if decoded_payload.strip():
                        stringlist2analyse.append(decoded_payload)

        string2analyse = " ".join(stringlist2analyse)
        if not stringlist2analyse:
            return []

        usehacks = self.config.getboolean(self.section, 'usehacks')
        headeruris = self.extractor.extracturis(string2analyse, use_hacks=usehacks)
        suspect.set_tag('headers.uris', headeruris)
        return headeruris

    def get_decoded_textparts_deprecated(self, suspect):
        """Returns a list of all text contents"""
        messagerep = suspect.get_message_rep()
        
        textparts=[]
        for part in messagerep.walk():
            if part.is_multipart():
                continue
            fname=part.get_filename(None)
            if fname is None:
                fname=""
            fname=fname.lower()
            contenttype=part.get_content_type()
            
            if contenttype.startswith('text/') or fname.endswith(".txt") or fname.endswith(".html") or fname.endswith(".htm"):
                payload=part.get_payload(None,True)
                if payload is not None:
                    # Try to decode using the given char set (or utf-8 by default)
                    charset = part.get_content_charset("utf-8")
                    payload = force_uString(payload,encodingGuess=charset)

                if 'html' in contenttype or '.htm' in fname: #remove newlines from html so we get uris spanning multiple lines
                    payload=payload.replace('\n', '').replace('\r', '')
                try:
                    payload = html.unescape(payload)
                except Exception:
                    self.logger.debug('%s failed to unescape html entities' % suspect.id)
                textparts.append(payload)
            
            if contenttype=='multipart/alternative':
                try:
                    payload = part.get_payload(None,True)

                    if payload is not None:
                        # Try to decode using the given char set
                        charset = part.get_content_charset("utf-8")
                        text = force_uString(payload,encodingGuess=charset)
                        textparts.append(text)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    self.logger.debug('%s failed to convert alternative part to string' % suspect.id)
            
        return textparts
    
    
    def lint(self):
        allok = True
        if not DOMAINMAGIC_AVAILABLE:
            print("ERROR: domainmagic lib or one of its dependencies (dnspython/pygeoip) is not installed!")
            allok = False
        
        if allok:
            allok = self.check_config()
        
        return allok



class EmailExtract(URIExtract):
    def __init__(self,config,section=None):
        URIExtract.__init__(self,config,section)
        self.logger = self._logger()

        # update the requiredvars dictionary inherited from URIExtract by additional values for EmailExtract
        self.requiredvars.update({
            'headers': {
                'default':'Return-Path,Reply-To,From,X-RocketYMMF,X-Original-Sender,Sender,X-Originating-Email,Envelope-From,Disposition-Notification-To', 
                'description':'comma separated list of headers to check for adresses to extract'
            },
            
            'skipheaders': {
                'default':'X-Original-To,Delivered-To,X-Delivered-To,Apparently-To,X-Apparently-To',
                'description':'comma separated list of headers with email adresses that should be skipped in body search'
            },
            
            'with_envelope_sender': {
                'default': 'True',
                'description': 'include envelope sender address as header address'
            }
        })
    
    
    def _run(self,suspect):
        if not DOMAINMAGIC_AVAILABLE:
            self.logger.info('Not scanning - Domainmagic not available')
            return DUNNO
        
        maxsize = self.config.getint(self.section, 'maxsize')
        maxsize_analyse = self.config.getint(self.section, 'maxsize_analyse')
        self._prepare()

        hrefs = []
        textparts=" ".join(self.get_decoded_textparts(suspect, ignore_words_without="@", maxsize=maxsize, maxsize_analyse=maxsize_analyse, hrefs=hrefs))
        body_emails = self.extractor.extractemails(textparts)

        # directly use mail addresses from html hrefs in atags
        hrefs = [h[len("mailto:"):] for h in hrefs if h.lower().startswith("mailto:")]
        body_emails.extend(hrefs)

        hdrs = ''
        for hdr in self.config.get(self.section, 'headers').split(','):
            hdrs += " " + " ".join(force_uString(suspect.get_message_rep().get_all(hdr, "")))
        hdr_emails = self.extractor.extractemails(hdrs)
        if self.config.getboolean(self.section, 'with_envelope_sender') and suspect.from_address:
            hdr_emails.append(suspect.from_address)

        ignoreemailtext=""
        for hdr in self.config.get(self.section,'skipheaders').split(','):
            ignoreemailtext += " " + " ".join(force_uString(suspect.get_message_rep().get_all(hdr,"")))
        ignoreemails=[x.lower() for x in self.extractor.extractemails(ignoreemailtext)]
        ignoreemails.extend(suspect.recipients)

        body_emails_final = []
        for e in body_emails:
            if e.lower() not in ignoreemails:
                body_emails_final.append(e)
                
        hdr_emails_final = []
        for e in hdr_emails:
            if e.lower() not in ignoreemails:
                hdr_emails_final.append(e)

        # make lists unique
        body_emails_final = list(set(body_emails_final))
        hdr_emails_final = list(set(hdr_emails_final))
        all_emails = list(set(body_emails_final + hdr_emails_final))

        suspect.set_tag('body.emails', body_emails_final)
        suspect.set_tag('header.emails', hdr_emails_final)
        suspect.set_tag('emails', all_emails)
        if self.config.getboolean(self.section,'loguris'):
            self.logger.info("Extracted emails: %s" % all_emails)
        
        return DUNNO


class DomainAction(ScannerPlugin):
    """Perform Action based on Domains in message body"""
    
    def __init__(self,config,section=None):
        ScannerPlugin.__init__(self,config,section)
        self.logger = self._logger()
    
        self.requiredvars={       
            'blacklistconfig':{
                'default':'/etc/fuglu/rbl.conf',
                'description':'Domainmagic RBL lookup config file',
            },
            'checksubdomains':{
                'default':'yes',
                'description':'check subdomains as well (from top to bottom, eg. example.com, bla.example.com, blubb.bla.example.com',
            },
            'action':{
                'default':'DUNNO',
                'description':'action on hit (dunno, reject, delete, etc)',
            },
            'message':{
                'default':'5.7.1 black listed URL ${domain} by ${blacklist}',
                'description':'message template for rejects/ok messages',
            },
            'maxlookups':{
                'default':'10',
                'description':'maximum number of domains to check per message',
            },
            'randomise':{
                'default':'False',
                'description':'randomise domain list before performing lookups',
            },
            'check_all':{
                'default':'False',
                'description':'if set to True do not abort on first hit, instead continue until maxlookups reached',
            },
            'extra_tld_file': {
                'default':'',
                'description':'path to file with extra TLDs (2TLD or inofficial TLDs)'
            },
            'testentry': {
                'default':'',
                'description': 'test record that should be included in at least one checked rbl (only used in lint)'
            },
            'exceptions_file': {
                'default':'',
                'description': 'path to file containing domains that should not be checked (one per line)'
            },
            'suspect_tags': {
                'default':'body.uris',
                'description': 'evaluate URIs listed in given tags (list tags white space separated)'
            },
        }
        
        self.rbllookup = None
        self.tldmagic = None
        self.extratlds = None
        self.lasttlds = None
        self.exceptions = None
        
        
    def _init_tldmagic(self):
        init_tldmagic = False
        extratlds = []
        
        if self.extratlds is None:
            extratldfile = self.config.get(self.section,'extra_tld_file')
            if extratldfile and os.path.exists(extratldfile):
                self.extratlds = FileList(extratldfile, lowercase=True)
                init_tldmagic = True
        
        if self.extratlds is not None:
            extratlds = self.extratlds.get_list()
            if self.lasttlds != extratlds: # extra tld file changed
                self.lasttlds = extratlds
                init_tldmagic = True
        
        if self.tldmagic is None or init_tldmagic:
            self.tldmagic = TLDMagic()
            for tld in extratlds: # add extra tlds to tldmagic
                self.tldmagic.add_tld(tld)
    
    
    def _check_skiplist(self, value):
        if self.exceptions is None:
            exceptionsfile = self.config.get(self.section, 'exceptions_file')
            if exceptionsfile and os.path.exists(exceptionsfile):
                self.exceptions = FileList(exceptionsfile, lowercase=True)
        
        if self.exceptions is not None:
            exceptionlist = self.exceptions.get_list()
            if value in exceptionlist:
                return True
        return False
    
    
    def _init_rbllookup(self):
        if self.rbllookup is None:
            blacklistconfig = self.config.get(self.section,'blacklistconfig')
            if os.path.exists(blacklistconfig):
                self.rbllookup = RBLLookup()
                self.rbllookup.from_config(blacklistconfig)
                
                
    def _get_uris(self, suspect):
        uris = []
        tags = self.config.get(self.section,'suspect_tags').split()
        for tag in tags:
            uris.extend(suspect.get_tag(tag, []))
        return uris
    
    
    def examine(self,suspect):
        if not DOMAINMAGIC_AVAILABLE:
            self.logger.info('Not scanning - Domainmagic not available')
            return DUNNO
        
        self._init_rbllookup()
        if self.rbllookup is None:
            self.logger.error('Not scanning - blacklistconfig could not be loaded')
            
        self._init_tldmagic()

        urls = self._get_uris(suspect)
        domains = set()
        for url in urls:
            try:
                domains.add(fqdn_from_uri(url))
            except Exception as e:
                self.logger.error(f"{suspect.id} (examine:fqdn_from_uri): {e} for uri: {url}")
        domains = list(domains)
        
        if self.config.getboolean(self.section, 'randomise'):
            domains = random.shuffle(domains)
        
        action = DUNNO
        message = None
        hits = {}
        counter=0
        self.logger.debug('%s checking domains %s' % (suspect.id, ', '.join(domains)))
        for domain in domains:
            if self._check_skiplist(domain):
                self.logger.debug('%s skipping lookup of %s (skiplisted)' % (suspect.id, domain))
                continue
            
            counter+=1
            if counter>self.config.getint(self.section,'maxlookups'):
                self.logger.info("%s maximum number of domains reached" % suspect.id)
                break
            
            tldcount=self.tldmagic.get_tld_count(domain)
            parts=domain.split('.')
            
            if self.config.getboolean(self.section,'checksubdomains'):
                subrange=range(tldcount+1,len(parts)+1)
            else:
                subrange=[tldcount+1]
            
            for subindex in subrange:
                subdomain='.'.join(parts[-subindex:])
                
                listings=self.rbllookup.listings(subdomain)
                for identifier,humanreadable in iter(listings.items()):
                    hits[domain] = identifier
                    suspect.set_tag('uri.rbl.listed', True)
                    suspect.set_tag('uri.rbl.address', domain)
                    suspect.set_tag('uri.rbl.list', identifier)
                    suspect.set_tag('uri.rbl.info', humanreadable)
                    self.logger.info("%s : URL host %s flagged as %s because %s"%(suspect.id,domain,identifier,humanreadable))
                    action = string_to_actioncode(self.config.get(self.section,'action'), self.config)
                    message = apply_template(self.config.get(self.section,'message'), suspect, dict(domain=domain,blacklist=identifier))
                    if not self.config.getboolean(self.section, 'check_all'):
                        return action, message
        
        suspect.set_tag('uri.rbl.allresults', hits)
        return action, message
    
    
    def lint(self):
        allok = True
        if not DOMAINMAGIC_AVAILABLE:
            print("ERROR: domainmagic lib or one of its dependencies (dnspython/pygeoip) is not installed!")
            allok = False
        
        if allok:
            allok = self.check_config()
        
        if allok:
            blconf = self.config.get(self.section,'blacklistconfig')
            if not blconf:
                allok = False
                print('ERROR: blacklistconfig not defined')
            elif not os.path.exists(blconf):
                allok = False
                print('ERROR: blacklistconfig %s not found' % blconf)
        
        if allok and self.config.has_option(self.section, 'extra_tld_file'):
            extratldfile = self.config.get(self.section,'extra_tld_file')
            if extratldfile and not os.path.exists(extratldfile):
                allok = False
                print('WARNING: extra_tld_file %s not found' % extratldfile)
                
        if allok and self.config.has_option(self.section, 'domainlist_file'):
            domainlist_file = self.config.get(self.section,'domainlist_file')
            if domainlist_file and not os.path.exists(domainlist_file):
                allok = False
                print('WARNING: domainlist_file %s not found' % domainlist_file)
                
        if allok:
            exceptionsfile = self.config.get(self.section, 'exceptions_file')
            if exceptionsfile and not os.path.exists(exceptionsfile):
                allok = False
                print('WARNING: exceptions_file %s not found' % exceptionsfile)
        
        testentry = self.config.get(self.section, 'testentry')
        if allok and testentry:
            self._init_rbllookup()
            listings = self.rbllookup.listings(testentry)
            if not listings:
                allok = False
                print('WARNING: test entry %s not found in any configured RBL zones' % testentry)
            else:
                print(listings)
                
        tags = self.config.get(self.section,'suspect_tags').split()
        print('INFO: checking URIs listed in tags: %s' % ' '.join(tags))
        
        return allok



class EmailAction(DomainAction):
    def __init__(self,config,section=None):
        DomainAction.__init__(self,config,section)
        self.domainlist = None
        del self.requiredvars['extra_tld_file']
        del self.requiredvars['checksubdomains']
        self.requiredvars['message']['default'] = '5.7.1 black listed email address ${address} by ${blacklist}'
        self.requiredvars['domainlist_file'] = {
            'default':'',
            'description':'path to file containing a list of domains. if specified, only query email addresses in these domains.'
        }
        self.requiredvars['exceptions_file']['description'] = 'path to file containing email addresses that should not be checked (one per line)'
        
    
    def _in_domainlist(self, email_address):
        domainlist_file = self.config.get(self.section,'domainlist_file').strip()
        if domainlist_file == '':
            return True
        
        if self.domainlist is None:
            self.domainlist = FileList(domainlist_file, lowercase=True)
        
        in_domainlist = False
        domain = domain_from_mail(email_address)
        if domain in self.domainlist.get_list():
            in_domainlist = True
        
        return in_domainlist
    
    
    def examine(self, suspect):
        if not DOMAINMAGIC_AVAILABLE:
            self.logger.info('Not scanning - Domainmagic not available')
            return DUNNO
        
        self._init_rbllookup()
        if self.rbllookup is None:
            self.logger.error('Not scanning - blacklistconfig could not be loaded')
        
        action = DUNNO
        message = None
        hits = {}
        checked = {}
        for addrtype in ['header.emails', 'body.emails']:
            addrs = suspect.get_tag(addrtype, [])
            if self.config.getboolean(self.section, 'randomise'):
                addrs = random.shuffle(addrs)
            
            for addr in addrs:
                if self._check_skiplist(addr):
                    self.logger.debug('%s skipping lookup of %s (skiplisted)' % (suspect.id, addr))
                    continue
                
                if not self._in_domainlist(addr):
                    self.logger.debug('%s skipping lookup of %s (not in domain list)' % (suspect.id, addr))
                    continue
                
                if len(checked) > self.config.getint(self.section, 'maxlookups'):
                    self.logger.info("%s maximum number of %s addresses reached" % (suspect.id, addrtype))
                    break
                
                try:
                    listings = checked[addr]
                except KeyError:
                    listings = self.rbllookup.listings(addr)
                    checked[addr] = listings
                
                for identifier, humanreadable in iter(listings.items()):
                    hits[addr] = identifier
                    suspect.set_tag('email.rbl.listed', True)
                    suspect.set_tag('email.rbl.type', addrtype)
                    suspect.set_tag('email.rbl.address', addr)
                    suspect.set_tag('email.rbl.list', identifier)
                    suspect.set_tag('email.rbl.info', humanreadable)
                    self.logger.info("%s : %s address %s flagged as %s because %s" % (suspect.id, addrtype, addr, identifier, humanreadable))
                    action = string_to_actioncode(self.config.get(self.section, 'action'), self.config)
                    message = apply_template(self.config.get(self.section, 'message'), suspect, dict(domain=addr, address=addr, blacklist=identifier))
                    if not self.config.getboolean(self.section, 'check_all'):
                        return action, message
        
        suspect.set_tag('uri.rbl.allresults', hits)
        return action, message



# --------- #
# Appenders #
# --------- #
class URIExtractAppender(URIExtract, AppenderPlugin):
    """Separate class to have a simple separate configuration section"""
    def process(self, suspect, decision):
        """If running as appender"""
        _ = self._run(suspect)


class EmailExtractAppender(EmailExtract, AppenderPlugin):
    """Separate class to have a simple separate configuration section"""
    def process(self, suspect, decision):
        """If running as appender"""
        _ = self._run(suspect)
