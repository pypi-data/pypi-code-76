# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utinni']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'utinni',
    'version': '0.5.0',
    'description': "Async client library for Empire's RESTful API ",
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/5151193/107455866-b6778d80-6b0c-11eb-9e7d-14221e2aa582.png" alt="Utinni" height="300"/>\n</p>\n\n# Utinni\n\nAn async Python client library for Empire\'s RESTful API \n\n(Only works with the [BC-Security Empire fork](https://github.com/BC-SECURITY/Empire))\n\n# Sponsors\n[<img src="https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png" width="130" height="130"/>](https://www.blackhillsinfosec.com/)\n[<img src="https://handbook.volkis.com.au/assets/img/Volkis_Logo_Brandpack.svg" width="130" hspace="10"/>](https://volkis.com.au)\n[<img src="https://user-images.githubusercontent.com/5151193/85817125-875e0880-b743-11ea-83e9-764cd55a29c5.png" width="200" vspace="21"/>](https://qomplx.com/blog/cyber/)\n[<img src="https://user-images.githubusercontent.com/5151193/86521020-9f0f4e00-be21-11ea-9256-836bc28e9d14.png" width="250" hspace="20"/>](https://ledgerops.com)\n[<img src="https://user-images.githubusercontent.com/5151193/102297674-e6d7ec80-3f0c-11eb-982f-cc5d13b0e9ce.jpg" width="250" hspace="20"/>](https://www.guidepointsecurity.com/)\n[<img src="https://user-images.githubusercontent.com/5151193/95542303-a27f1c00-09b2-11eb-8682-e10b3e0f0710.jpg" width="200" hspace="20"/>](https://lostrabbitlabs.com/)\n\n# Table of Contents\n\n* [Utinni](#utinni)\n  + [Installing](#installing)\n  + [Examples](#examples)\n  + [FAQ](#faq)\n\n## Installing\n\n`pip3 install utinni`\n\n## Examples\n\nSee the [examples](/../master/src/examples) folder for more.\n\nSimple example showing basic usage:\n\n```python\nimport asyncio\nfrom utinni import EmpireApiClient\n\nasync def main():\n    # Create client instance\n    empire = EmpireApiClient(host="localhost", port="1337")\n\n    # Login to Empire\'s RESTful API\n    await empire.login("username", "password")\n    print("* Logged into Empire")\n\n    # Create a listener\n    await empire.listeners.create(listener_type="http", name="Utinni", additional={"Port": 8443})\n\n    print("* Waiting for agents...")\n    while True:\n        # Poll for new agents every 1 sec\n        for agent in await empire.agents.get():\n\n            #Print some basic info on the new agent\n            print(f"+ New agent \'{agent.name}\' connected: {agent.domain}\\\\{agent.username}")\n\n            # Execute a module on the agent\n            module_output = await agent.execute(\n                    "powershell/lateral_movement/invoke_wmi",\n                    options={\n                        "ComputerName": "targethost",\n                        "Listener": "Utinni",\n                    },\n                )\n\n            print(f"++ Executed invoke_wmi module on agent \'{agent.name}\'")\n            print(f"++ Module output: {module_output}")\n\n        await asyncio.sleep(1)\n\n# Start the event loop\nasyncio.run(main())\n```\n\nExample with background tasks:\n\n```python\nimport asyncio\nfrom utinni import EmpireApiClient\n\nasync def agent_poller(empire):\n    # Poll for new agents every 1 sec\n    print("* Waiting for agents...")\n    while True:\n        for agent in await empire.agents.get():\n            #Print some basic info on the new agent\n            print(f"+ New agent \'{agent.name}\' connected: {agent.domain}\\\\{agent.username}")\n\n            # Do whatever you want with the agent object here and it won\'t block the main thread\n            # In this example executing we\'re executing a shell command\n            cmd_output = await agent.shell("dir")\n\n            print("++ Executed shell command")\n            print(f"++ Output: {cmd_output}")\n\n        await asyncio.sleep(1)\n\nasync def main():\n    # Create client instance\n    empire = EmpireApiClient(host="localhost", port="1337")\n\n    # Login to Empire\'s RESTful API\n    await empire.login("username", "password")\n    print("* Logged into Empire")\n\n    # Create a listener\n    await empire.listeners.create(listener_type="http", name="Utinni", additional={"Port": 8443})\n\n    # Start the \'agent_poller\' coroutine as a background task \n    agent_poller_task = asyncio.create_task(agent_poller(empire))\n\n    # Do more stuff here as this thread isn\'t blocked.\n    available_empire_modules = await empire.modules.get()\n\n    # Wait for the agent_poller_task to complete\n    # in this example it won\'t ever finish since it\'s in a infinite loop.\n    await agent_poller_task\n\n# Start the event loop\nasyncio.run(main())\n```\n\n## FAQ\n\n**1. Why?**\n\nThis was originally made for the [DeathStar](https://github.com/byt3bl33d3r/DeathStar) project, the author then realized it would be useful as a stand-alone library.\n\n**2. Why doesn\'t this library provide a sync API?**\n\nCause it doesn\'t make sense. In 99% of all use cases you\'re going to want to call/execute/query/do multiple things at the same time. This is legitimately the perfect use case of AsyncIO.\n\n**3. Will this work with the original Empire repository and not the BC-Security Fork?**\n\nProbably not. You\'re welcome to try though.',
    'author': 'Marcello Salvati',
    'author_email': 'byt3bl33d3r@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/byt3bl33d3r/Utinni',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
