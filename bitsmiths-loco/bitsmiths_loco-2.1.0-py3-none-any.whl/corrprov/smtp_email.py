# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import datetime
import smtplib
import os.path

import email.encoders
import email.mime.base
import email.mime.multipart
import email.mime.text
import email.mime.image

from bs_lib.Pod   import Pod

from bs_loco.db   import tMsg

from .provider_email import ProviderEmail

from bs_lib  import Common


class SmtpEmail(ProviderEmail):
    """
    The standard SMTP email provider.
    """

    def __init__(self):
        """
        Constructor.
        """
        ProviderEmail.__init__(self)
        self._smtp = None


    def id(self) -> str:
        """
        Overload.
        """
        return 'smtp'


    def destroy(self):
        """!
        Cleans up the provider.
        """
        self._logoff()
        ProviderEmail.destroy(self)


    def initialize(self, pod: Pod, dao: object, cfg: dict):
        """
        Overload.
        """
        ProviderEmail.initialize(self, pod, dao, cfg)

        Common.readDict(self._cfg, 'host',        str)
        Common.readDict(self._cfg, 'port',        int)
        Common.readDict(self._cfg, 'username',    str)
        Common.readDict(self._cfg, 'passwd',      str)
        Common.readDict(self._cfg, 'from',        str)
        Common.readDict(self._cfg, 'ssl',         bool)
        Common.readDict(self._cfg, 'tls',         bool)
        Common.readDict(self._cfg, 'timeout',     float)


    def _logoff(self):
        """
        Log off of the smtp server.
        """
        if self._smtp:
            try:
                self._smtp.quit()
            except smtplib.SMTPServerDisconnected as x:
                self._log.warning('Smtp already disconnected in destroy: %s' % str(x))
            finally:
                self._smtp = None


    def _login(self):
        """
        Log onto the smtp server.
        """
        self._logoff()

        if self._cfg.get('ssl'):
            self._smtp = smtplib.SMTP_SSL(self._cfg['host'], self._cfg['port'], timeout=self._cfg['timeout'])
        else:
            self._smtp = smtplib.SMTP(self._cfg['host'], self._cfg['port'], self._cfg['timeout'])

        if self._cfg.get('tls'):
            self._smtp.starttls()

        # ensure we can login
        if len(self._cfg['username']) < 1:
            raise Exception('Cannot log into smtp server without a user name!')

        self._smtp.login(os.path.expandvars(self._cfg['username']), os.path.expandvars(self._cfg['passwd']))

        self._log.debug('smtp initialized [host:%s, user:%s]' % (self._cfg['host'], self._cfg['username']))


    def _provider_send(self, payload: dict, res_list: list, msg: tMsg, addr_list: list) -> tuple:
        """
        Overload.
        """
        try:
            dtstart = datetime.datetime.now()

            self._login()

            emsg = email.mime.multipart.MIMEMultipart('related')

            emsg['Subject'] = payload['subject']
            emsg['From']    = self._cfg['from']
            emsg['To']      = ';'.join(addr_list)
            emsg['Date']    = email.utils.formatdate(localtime=True)
            emsg.preamble   = 'This is a multi-part message in MIME format.'

            msg_alt = email.mime.multipart.MIMEMultipart('alternative')
            emsg.attach(msg_alt)

            msg_alt.attach(email.mime.text.MIMEText(payload['body-html'], 'html'))
            msg_alt.attach(email.mime.text.MIMEText(payload['body-text']))

            if res_list:
                for att in res_list:
                    if not att.content or not att.mimetype or not att.mimetype.startswith('image/'):
                        continue

                    att_img = email.mime.image.MIMEImage(att.content)
                    att_img.add_header('Content-ID', '<{}>'.format(att.id))
                    emsg.attach(att_img)

                for att in res_list:
                    if not att.content or (att.mimetype and att.mimetype.startswith('image/')):
                        continue

                mtype             = att.mimetype or 'application/octet-stream'
                maintype, subtype = mtype.split('/', 1)

                part = email.mime.base.MIMEBase(maintype, subtype)
                part.set_payload(att.content)

                email.encoders.encode_base64(part)

                part.add_header('Content-Disposition', 'attachment', filename = att.filename)
                emsg.attach(part)

            self._smtp.sendmail(self._cfg['from'], addr_list, emsg.as_string())

            dtend = datetime.datetime.now()

            self._log.debug(' - mail sent successfull')
        except Exception as x:
            self._log.error('Exception caught sending email [%s]' % (str(msg)))
            self._log.exception(x)
            return (False, None, str(x))
        finally:
            self._logoff()

        return (True, dtend - dtstart, None)
