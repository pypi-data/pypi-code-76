# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgpy', 'bgpy.core', 'bgpy.example']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.4.0,<4.0.0']}

entry_points = \
{'console_scripts': ['bgpy = bgpy.cli:main']}

setup_kwargs = {
    'name': 'bgpy',
    'version': '0.2.0',
    'description': 'Running local or remote Python servers in the background and establish stream socket-based communication with clients.',
    'long_description': '\n====\nbgpy\n====\n\n.. image:: https://img.shields.io/pypi/v/bgpy.svg\n        :target: https://pypi.python.org/pypi/bgpy\n\n.. image:: https://github.com/munterfinger/bgpy/workflows/check/badge.svg\n        :target: https://github.com/munterfinger/bgpy/actions?query=workflow%3Acheck\n\n.. image:: https://readthedocs.org/projects/bgpy/badge/?version=latest\n        :target: https://bgpy.readthedocs.io/en/latest/\n        :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/munterfinger/bgpy/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/munterfinger/bgpy\n\n\nRunning local or remote Python servers in the background using the subprocess\nmodule and establish stream socket-based communication with clients in both\ndirections.\n\nFeatures:\n\n* Start and initialize a server process with a simple Python script. Once this\n  parent script is terminated, the server process continues to run in the\n  background.\n* Send Python objects between the server and client processes (stored in a\n  :code:`dict`) without worrying about serialization, setting up server and\n  client sockets, message length, and chunksize in the network buffer.\n* Due to the socket-based communication between server and client, it is\n  possible to resume the communication from any location, as long as access to\n  the same network is given and the hostname and port on which the server is\n  listening is known.\n* The communication between client and server is operating system independent\n  (not like FIFO pipes for example). Furthermore, on Windows it is possible to\n  communicate between the Windows Subsystem for Linux (WSL) and the Windows\n  host system using bgpy.\n* Optionally start the server on the remote using the command line interface\n  (:code:`bgpy server <host> <port>`), and initialize it from the local client\n  (:code:`initialize(host, port, init_task, exec_task, exit_task)`) using\n  Python.\n\nGetting started\n---------------\n\nInstall the stable release of the package from pypi:\n\n.. code-block:: shell\n\n    pip install bgpy\n\nDefine tasks\n^^^^^^^^^^^^\n\nRun and intialize a bgpy server on a host, which starts listening\nto the provided port. After starting the server, a INIT message with the\n:code:`init_task`, :code:`exec_task()` and :code:`exit_task()` tasks are send\nto the server in order to complete the initialization.\n\n* **Initialization task**\n\nTask that runs once during initialization and can be used to set up the\nserver. The return value of this function must be a dict, which is then\npassed to the :code:`exec_task` function with every request by a client.\n\n.. code-block:: python\n    \n    def init_task(client_socket: ClientSocket) -> dict:\n        init_args = {"request_count": 0, "value": 1000}\n        return init_args\n\n* **Execution task**\n\nTask that is called each time a request is made by a client to the server.\nIn this task the message from the :code:`execute` method of the :code:`Client`\nclass is interpreted and an action has to be defined accordingly. The\ninput of the :code:`exec_task` is the return value of the last\n:code:`exec_task` function call (or if never called, the return value from the\n:code:`init_task`). Using the function :code:`respond` om the server, a second\nresponse can be sent to the client after the standard confirmation of the\nreceipt of the message by the server.\n\n.. code-block:: python\n    \n    def exec_task(\n        client_socket: ClientSocket, init_args: dict, exec_args: dict\n    ) -> dict:\n        init_args["request_count"] += 1\n        if exec_args["command"] == "increase":\n                init_args["value"] += exec_args["value_change"]\n        if exec_args["command"] == "decrease":\n                init_args["value"] -= exec_args["value_change"]\n        return init_args\n\n* **Exit task**\n\nTask that is executed once if an exit message is sent to the server by\nthe :code:`terminate` method of the :code:`Client` class. The input of the\n:code:`exit_task` is the return value of the last :code:`exec_task` function\ncall (or if never called, the return value from the :code:`init_task`). With\n:code:`respond` a second message can be sent to the client, if the client is\nset to be waiting for a second response\n(:code:`Client.terminate(..., await_response=True`).\n\n.. code-block:: python\n    \n    def exit_task(\n        client_socket: ClientSocket, init_args: dict, exit_args: dict\n    ) -> None:\n        init_args["request_count"] += 1\n        init_args["status"] = "Exited."\n        respond(client_socket, init_args)\n        return None\n\n**Note:** If the client is set to wait for a second response\n(:code:`Client.execute(..., await_response=True` or\n:code:`Client.terminate(..., await_response=True`) it is important to handle\nthis on the server side by sending a response to the client using\n:code:`respond`. Otherwise the client may be waiting forever as there is no\ntimeout specified.\n\n\nRun the server\n^^^^^^^^^^^^^^\n\nRun an example background process on localhost and send requests using client\nsockets:\n\n.. code-block:: python\n\n    from bgpy import Client, Server\n    from bgpy.example.tasks import init_task, exec_task, exit_task\n\n    HOST = "127.0.0.1"\n    PORT = 54321\n\n    # Create server context\n    server = Server(host=HOST, port=PORT)\n\n    # Start server in background from context\n    server.run_background()\n\n    # Bind client to server context\n    client = Client(host=HOST, port=PORT)\n\n    # Send INIT message from client to server, receive OK\n    response = client.initialize(init_task, exec_task, exit_task)\n\n    # Execute command \'increase\' with value on server, receive OK\n    response = client.execute({"command": "increase", "value_change": 10})\n\n    # Execute command \'decrease\' with value on server, receive OK\n    response = client.execute({"command": "decrease", "value_change": 100})\n\n    # Terminate and wait for response, receive OK with values\n    response = client.terminate(await_response=True)\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE file for\ndetails.\n',
    'author': 'Merlin Unterfinger',
    'author_email': 'info@munterfinger.ch',
    'maintainer': 'Merlin Unterfinger',
    'maintainer_email': 'info@munterfinger.ch',
    'url': 'https://pypi.org/project/bgpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
