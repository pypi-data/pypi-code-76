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

from .loco_trig_async import LocoTrigAsync


class StubAsync(LocoTrigAsync):
    """
    This is the stub class for firing off loco message requests
    into the system.
    """

    def __init__(self):
        """
        Constructor.
        """
        LocoTrigAsync.__init__(self)


    def id(self) -> str:
        """
        Overload.
        """
        raise 'stub[async]'


    def name(self) -> str:
        """
        Overload.
        """
        'Stub [Async]'


    async def _trigger(self,
                       notype    : str,
                       corr_addr : dict,
                       key_pair  : dict = None,
                       res       : dict = None,
                       meta_data : dict = None) -> int:
        print('Loco Stub Async - notype:%s, corr_addr:%r, key_pair:%r, res:%r, meta_data:%r' % (
            notype, corr_addr, key_pair, res, meta_data))
