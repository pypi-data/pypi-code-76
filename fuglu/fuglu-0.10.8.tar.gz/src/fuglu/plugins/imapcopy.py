# -*- coding: UTF-8 -*-
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
from fuglu.shared import ScannerPlugin, DUNNO, DELETE, SuspectFilter
from fuglu.stringencode import force_uString
import os
import imaplib
from urllib.parse import urlparse


#TODO: reuse imap connections
#TODO: 'problemaction', retries
#TODO: appender

class IMAPCopyPlugin(ScannerPlugin):
    """This plugins stores a copy of the message to an IMAP mailbox if it matches certain criteria (Suspect Filter).
The rulefile works similar to the archive plugin. As third column you have to provide imap account data in the form:

<protocol>://<username>:<password>@<servernameorip>[:port]/<mailbox>

<protocol> is one of:
 - imap (port 143, no encryption)
 - imap+tls (port 143 and StartTLS, only supported in Python 3)
 - imaps (port 993 and SSL)


"""
    def __init__(self,config,section=None):
        ScannerPlugin.__init__(self,config,section)
        
        self.requiredvars = {
            'imapcopyrules': {
                'default': '/etc/fuglu/imapcopy.regex',
                'description': 'IMAP copy suspectFilter File',
            },
            
            'storeoriginal': {
                'default': 'True',
                'description': "if true/1/yes: store original message\nif false/0/no: store message probably altered by previous plugins, eg with spamassassin headers",
            },
        }
        self.filter=None
        self.logger=self._logger()

        
    def examine(self,suspect):
        imapcopyrules=self.config.get(self.section, 'imapcopyrules')
        if imapcopyrules is None or imapcopyrules=="":
            return DUNNO
        
        if not os.path.exists(imapcopyrules):
            self._logger().error('IMAP copy rules file does not exist : %s'%imapcopyrules)
            return DUNNO
        
        if self.filter is None:
            self.filter=SuspectFilter(imapcopyrules)
        
        (match,info)=self.filter.matches(suspect,extended=True)
        if match:
            delete = False
            field,matchedvalue,arg,regex=info
            if arg is not None and arg.lower()=='no':
                suspect.debug("Suspect matches imap copy exception rule")
                self.logger.info("""%s: Header %s matches imap copy exception rule '%s' """%(suspect.id,field,regex))
            else:
                if arg is None or (not arg.lower().startswith('imap') and arg != 'DELETE'):
                    self.logger.error("Unknown target format '%s' should be 'imap(s)://user:pass@host/folder'"%arg)
                    
                else:
                    self.logger.info("""%s: Header %s matches imap copy rule '%s' """%(suspect.id,field,regex))
                    if suspect.get_tag('debug'):
                        suspect.debug("Suspect matches imap copy rule (I would copy it if we weren't in debug mode)")
                    else:
                        if ' ' not in arg:
                            if arg.lower() != 'delete':
                                self.storeimap(suspect, arg)
                            else:
                                return DUNNO
                        else:
                            for value in arg.split():
                                if value == 'DELETE':
                                    self.logger.info("""%s: imap copy rule '%s' action DELETE""" % (suspect.id, regex))
                                    delete = True
                                    continue
                                self.storeimap(suspect, value)
                    if delete: return DELETE
        else:
            suspect.debug("No imap copy rule/exception rule applies to this message")
        return DUNNO
    
    
    def imapconnect(self,imapurl,lintmode=False):
        p=urlparse(imapurl)
        scheme=p.scheme.lower()
        host=p.hostname
        port=p.port
        username=p.username
        password=p.password
        folder=p.path[1:]
        
        if scheme == 'imaps':
            ssl = True
            tls = False
        elif scheme == 'imap+tls':
            ssl=False
            tls = True
        else:
            ssl = False
            tls = False
        
        
        if port is None:
            if ssl:
                port=imaplib.IMAP4_SSL_PORT
            else:
                port=imaplib.IMAP4_PORT
        try:
            if ssl:
                imap=imaplib.IMAP4_SSL(host=host,port=port)
            else:
                imap=imaplib.IMAP4(host=host,port=port)
        except Exception as e:
            ltype='IMAP'
            if ssl:
                ltype='IMAP-SSL'
            msg="%s Connection to server %s failed: %s" % (ltype, host, force_uString(e.args[0]))
            if lintmode:
                print(msg)
            else:
                self.logger.error(msg)
            return None
        
        if tls and hasattr(imap, 'starttls'):
            try:
                msg = imap.starttls()
                if msg[0] != 'OK':
                    if lintmode:
                        print(msg)
                    return None
                    
            except Exception as e:
                if lintmode:
                    print(str(e))
                return None
            
        try:
            imap.login(username, password)
        except Exception as e:
            msg="Login to server %s failed for user %s: %s" % (host, username, force_uString(e.args[0]))
            if lintmode:
                print(msg)
            else:
                self.logger.error(msg)
            return None
        
        try:
            mtype, count = imap.select(folder)
            excmsg = ''
        except Exception as e:
            excmsg = str(e)
            mtype = None
            
        if mtype=='NO' or excmsg:
            msg="Could not select folder %s@%s/%s : %s" % (username, host, folder, excmsg)
            if lintmode:
                print(msg)
            else:
                self.logger.error(msg)
            return None
        return imap
        
    
    def storeimap(self,suspect,imapurl):
        imap=self.imapconnect(imapurl)
        if not imap:
            return
        #imap.debug=4
        p=urlparse(imapurl)
        folder=p.path[1:]
        
        if self.config.getboolean(self.section,'storeoriginal'):
            src=suspect.get_original_source()
        else:
            src=suspect.get_source()

        mtype, data = imap.append(folder,None,None,src)
        if mtype!='OK':
            self.logger.error('Could put store in IMAP. APPEND command failed: %s' % data)
        imap.logout()



    def lint(self):
        allok=(self.check_config() and self.lint_imap())
        return allok

    def lint_imap(self):
        #read file, check for all imap accounts
        imapcopyrules=self.config.get(self.section, 'imapcopyrules')
        if imapcopyrules!='' and not os.path.exists(imapcopyrules):
            print("Imap copy rules file does not exist : %s"%imapcopyrules)
            return False
        sfilter=SuspectFilter(imapcopyrules)

        accounts=[]
        for tup in sfilter.patterns:
            headername,pattern,arg = tup
            if arg not in accounts:
                if arg is None:
                    print("Rule %s %s has no imap copy target" % (headername, pattern.pattern))
                    return False
                if arg.lower()=='no':
                    continue
                elif arg.lower() == 'delete':
                    return False
                if ' ' not in arg:
                    accounts.append(arg)
                else:
                    for value in arg.split():
                        if value == 'DELETE': continue
                        accounts.append(value)
        
        success = True
        for acc in accounts:
            msg = 'OK'
            p=urlparse(acc)
            host=p.hostname
            username=p.username
            folder=p.path[1:]
            try:
                imap=self.imapconnect(acc,lintmode=True)
                if not imap:
                    msg = 'ERROR: Failed to connect'
                    success = False
            except Exception as e:
                msg = 'ERROR: %s' % str(e)
            print("Checked %s@%s/%s : %s" % (username, host, folder, msg))
        if not success:
            return False

        return True
