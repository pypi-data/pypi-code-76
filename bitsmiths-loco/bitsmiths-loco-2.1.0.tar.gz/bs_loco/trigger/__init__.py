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

from bs_lib import Pod, PodAsync

from bs_loco           import constants
from bs_loco.xloco     import xLoco

from .loco_trig      import LocoTrig
from .local_db       import LocalDB
from .stub           import Stub

from .loco_trig_async  import LocoTrigAsync
from .local_db_async   import LocalDBAsync
from .stub_async       import StubAsync


def get_trigger(pod: Pod, trig_id: str, cfg: dict = None) -> LocoTrig:
    """
    Factory to load a loco trigger by id.

    :param pod: The pod to use.
    :param trig_id: Loco trigger identifier.
    :param cfg: The trigger config object
    """
    res = None

    if trig_id == constants.LOCO_TRIGGER_LOCAL_DB:
        res = LocalDB()
    elif trig_id == constants.LOCO_TRIGGER_STUB:
        res = Stub()
    # TODO, add kafka queue or other mechanisms here

    if not res:
        raise xLoco('Loco Trigger [%s] not expected.' % trig_id)

    res.initialize(pod, cfg)

    if res.is_deadbeef():
        del res
        res = Stub()
        res.initialize(pod, cfg)

    return res


async def get_trigger_async(pod: PodAsync, trig_id: str, cfg: dict = None) -> LocoTrigAsync:
    """
    Factory to load am async loco trigger by id.

    :param pod: The pod to use.
    :param trig_id: Loco trigger identifier.
    :param cfg: The trigger config object
    """
    res = None

    if trig_id == constants.LOCO_TRIGGER_LOCAL_DB:
        res = LocalDBAsync()
    elif trig_id == constants.LOCO_TRIGGER_STUB:
        res = StubAsync()
    # TODO, add kafka queue or other mechanisms here

    if not res:
        raise xLoco('Loco Trigger [%s] not expected.' % trig_id)

    await res.initialize(pod, cfg)

    if res.is_deadbeef():
        del res
        res = StubAsync()
        await res.initialize(pod, cfg)

    return res
