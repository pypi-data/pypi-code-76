#     ____        _           
#    / __ \____ _(_)______  __
#   / / / / __ `/ / ___/ / / /
#  / /_/ / /_/ / (__  ) /_/ / 
# /_____/\__,_/_/____/\__, /  
# martin shishkov    /____/   
#
#   Copyright 2020 Martin Shishkov, gulliversoft.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from time import sleep
 
from rocket.daisy.utils.version import BOARD_REVISION, VERSION
from rocket.daisy.utils.logger import setInfo, setDebug, info, debug, warn, error, exception
from rocket.daisy.utils.thread import runLoop
from rocket.daisy.server import Server
from rocket.daisy.devices.instance import deviceInstance
from rocket.daisy.decorators.rest import macro

from rocket.daisy.devices import bus as _bus


try:
    import _daisy.GPIO as GPIO
except:
    pass


setInfo()
_bus.checkAllBus()
