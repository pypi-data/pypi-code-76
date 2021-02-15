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
from bs_loco       import constants
from bs_loco.xloco import xLoco

from bs_loco.db.tables   import tMsgReq

from .provider import Provider


class ProviderEmail(Provider):
    """
    This is the base email provder overload.
    """

    def __init__(self):
        """
        Constructor.
        """
        Provider.__init__(self)


    def corrtype_id(self) -> str:
        """
        Overload.
        """
        return constants.CORRTYPE_EMAIL


    def _build_payload(self, req: tMsgReq) -> dict:
        """
        Overload.
        """
        templ = self._cache['templ'][req.notype_id]
        kpair = self._build_msg_keypairs(req)

        return {
            'subject'   : self._template_subst(templ.get('subject'),   kpair),
            'body-html' : self._template_subst(templ.get('body-html'), kpair),
            'body-text' : self._template_subst(templ.get('body-text'), kpair),
        }


    def _validate_template(self, templ: dict) -> dict:
        """
        Overload.
        """
        for val in [ 'subject', 'body-html', 'body-text' ]:
            obj = templ.get(val)

            if not obj:
                raise xLoco('Invalid email template, [%s] missing or empty [corrprov:%s, corrtype:%s, templ:%s]' % (
                    val, self.id(), self.corrtype_id(), str(templ)))

        return templ
