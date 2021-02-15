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
from bs_lib import Pod

from .base_loco_trig import BaseLocoTrig


class LocoTrig(BaseLocoTrig):
    """
    This is the base class for firing off loco message requests
    into the system.
    """

    def __init__(self):
        """
        Constructor.
        """
        BaseLocoTrig.__init__(self)


    def __del__(self):
        """
        Destructor.
        """
        self.destroy()


    def initialize(self, pod: Pod, cfg: dict):
        """
        Virtual method to initialize the loco trigger interface.

        :param pod: The pod to use.
        :param cfg: Any configs needed for the trigger, can be None.
        """
        self.destroy()
        self._pod = pod
        self._cfg = cfg


    def destroy(self):
        """
        Virtual method to destroy the content management object.
        """
        self._pod = None
        self._cfg = None


    def trig(self,
             notype    : str,
             corr_addr : dict,
             key_pair  : dict = None,
             res       : dict = None,
             meta_data : dict = None) -> int:
        """
        Wrapper method that validates and then triggers a new correspondence message to correspondence addresses.

        :param notype: The notification type identifier.
        :param corr_addr: The addresses for each correspondence type required.
        :param key_pair: Additional data dictionary to use for messsage subsitution.
        :param res: And additional file resources to add to the out going correspondence.
        :param meta_data: Optional meta data.
        :return: The number of correspondence messages queued.
        """
        self._validate_dict(self.SCHEMA_ADDR, corr_addr, 'corr_addr', True)
        self._validate_dict(self.SCHEMA_RESOURCE, res, 'res', False)

        return self._trigger(notype, corr_addr, key_pair, res, meta_data)


    def _trigger(self,
                 notype    : str,
                 corr_addr : dict,
                 key_pair  : dict = None,
                 res       : dict = None,
                 meta_data : dict = None) -> int:
        """
        Pure virtual method that triggers the actual correspondence messages.

        :param notype: The notification type identifier.
        :param corr_addr: The addresses for each correspondence type required.
        :param key_pair: Additional data dictionary to use for messsage subsitution.
        :param res: And additional file resources to add to the out going correspondence.
        :param meta_data: Optional meta data for the trigger.
        :return: The number of correspondence messages queued.
        """
        raise Exception('_trigger() not implemented.')
