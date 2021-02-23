"""
Zserio Python runtime library

.. data:: VERSION_STRING

   Zserio Python runtime library version string.
"""

from zserio.bitbuffer import BitBuffer
from zserio.bitreader import BitStreamReader
from zserio.bitwriter import BitStreamWriter
from zserio.exception import PythonRuntimeException
from zserio.service import ServiceInterface, ServiceException
from zserio.pubsub import PubsubInterface, PubsubException

import zserio.array
import zserio.bitfield
import zserio.bitposition
import zserio.bitsizeof
import zserio.builtin
import zserio.float
import zserio.hashcode
import zserio.limits

VERSION_STRING = "2.1.0"

"""
Zserio runtime library extension built in PyPi package.
"""

from zserio.compiler import JavaNotFoundException, runCompiler, generatePython, generate
