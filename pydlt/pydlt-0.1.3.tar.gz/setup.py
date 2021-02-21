# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydlt', 'pydlt.control']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydlt',
    'version': '0.1.3',
    'description': 'A pyre-python library to handle AUTOSAR DLT.',
    'long_description': '# PyDLT\n\nA pyre-python library to handle AUTOSAR DLT protocol, which is based on\nAUTOSAR Specification of Diagnostic Log and Trace V1.2.0 R4.0 Rev3, Section 7.7 Protocol Specification.\n\n## Quick Start\n\n### Write messages to DLT file\n\n```py\nfrom pydlt import (\n    ArgumentString,\n    DltFileWriter,\n    DltMessage,\n    MessageLogInfo,\n    MessageType,\n    StorageHeader,\n)\n\n# Create DLT message\nmsg1 = DltMessage.create_verbose_message(\n    [ArgumentString("hello, pydlt!")],\n    MessageType.DLT_TYPE_LOG,\n    MessageLogInfo.DLT_LOG_INFO,\n    "App",\n    "Ctx",\n    message_counter=0,\n    str_header=StorageHeader(0, 0, "Ecu"),\n)\nprint(msg1)\n# > 1970/01/01 09:00:00.000000 0 Ecu App Ctx log info verbose 1 hello, pydlt!\nmsg2 = DltMessage.create_non_verbose_message(\n    0,\n    b"\\x01\\x02\\x03",\n    message_counter=1,\n    str_header=StorageHeader(0, 0, "Ecu"),\n)\nprint(msg2)\n# > 1970/01/01 09:00:00.000000 1 Ecu non-verbose [0] 010203\n\n# Write DLT messages to file\nwith DltFileWriter("<path to DLT file>") as writer:\n    writer.write_messages([msg1, msg2])\n```\n\n### Read messages from DLT file\n\n```py\nfrom pydlt import DltFileReader\n\n# Read DLT messages from file\nfor msg in DltFileReader("<path to DLT file>"):\n    # Print overview of each DLT message\n    print(msg)\n```\n\n## Limitation\n\nThe following format of Type Info in a Payload has not been supported.\n\n- TYPE_LENGTH_128BIT\n- TYPE_ARRAY\n- VARIABLE_INFO\n- FIXED_POINT\n- TRACE_INFO\n- TYPE_STRUCT\n',
    'author': 'Miki, Hiromitsu',
    'author_email': 'mikiepure+dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mikiepure.github.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
