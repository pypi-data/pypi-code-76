# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapapi',
 'yapapi._cli',
 'yapapi.executor',
 'yapapi.package',
 'yapapi.props',
 'yapapi.rest',
 'yapapi.storage']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-sse-client>=0.1.7,<0.2.0',
 'aiohttp>=3.6,<4.0',
 'async_exit_stack>=1.0.1,<2.0.0',
 'jsonrpc-base>=1.0.3,<2.0.0',
 'more-itertools>=8.6.0,<9.0.0',
 'srvresolver>=0.3.5,<0.4.0',
 'toml>=0.10.1,<0.11.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'urllib3>=1.25.9,<2.0.0',
 'ya-aioclient>=0.5.0,<0.6.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'cli': ['fire>=0.3.1,<0.4.0', 'rich>=2.2.5,<3.0.0']}

setup_kwargs = {
    'name': 'yapapi',
    'version': '0.5.0',
    'description': 'High-level Python API for the New Golem',
    'long_description': '# Golem Python API\n\n[![Tests - Status](https://img.shields.io/github/workflow/status/golemfactory/yapapi/Continuous%20integration/master?label=tests)](https://github.com/golemfactory/yapapi/actions?query=workflow%3A%22Continuous+integration%22+branch%3Amaster)\n![PyPI - Status](https://img.shields.io/pypi/status/yapapi)\n[![PyPI version](https://badge.fury.io/py/yapapi.svg)](https://badge.fury.io/py/yapapi)\n[![GitHub license](https://img.shields.io/github/license/golemfactory/yapapi)](https://github.com/golemfactory/yapapi/blob/master/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/golemfactory/yapapi)](https://github.com/golemfactory/yapapi/issues)\n\n## What\'s Golem, btw?\n\n[Golem](https://golem.network) is a global, open-source, decentralized supercomputer\nthat anyone can access. It connects individual machines - be that laptops, home PCs or\neven data centers - to form a vast network, the purpose of which is to provide a way to\ndistribute computations to its provider nodes and allow requestors to utilize its unique\npotential - which can lie in its combined computing power, the geographical distribution\nor its censorship resistance.\n\n## Golem\'s requestor setup\n\nGolem\'s requestor-side configuration consists of two separate components:\n* the [`yagna` daemon](https://github.com/golemfactory/yagna) - your node in the\n  new Golem network, responsible for communication with the other nodes, running the\n  market and providing easy access to the payment mechanisms.\n* the requestor agent - the part that the developer of the specific Golem application\n  is responsible for.\n\nThe daemon and the requestor agent communicate using three REST APIs which\n`yapapi` - Golem\'s Python high-level API - aims to abstract to large extent to make\napplication development on Golem as easy as possible.\n\n## How to use this API?\n\nAssuming you have your Golem node up and running (you can find instructions on how to\ndo that in the [yagna repository](https://github.com/golemfactory/yagna) and in our\n[handbook](https://handbook.golem.network)), what you need to do is:\n* **prepare your payload** - this needs to be a Docker image containing your application\n  that will be executed on the provider\'s end. This image needs to have its volumes\n  mapped in a way that will allow the supervisor module to exchange data (write and\n  read files) with it. This image needs to be packed and uploaded into Golem\'s image repository\n  using our dedicated tool - [`gvmkit-build`](https://pypi.org/project/gvmkit-build/).\n* **create your requestor agent** - this is where `yapapi` comes in. Utilizing our high-level\n  API, the creation of a requestor agent should be straighforward and require minimal effort.\n  You can use examples contained in this repository (blender and hashcat) as references.\n\n### Components\n\nThere are a few components that are crucial for any requestor agent app:\n\n#### Executor\n\nThe heart of the high-level API is the requestor\'s task executor (`yapapi.Executor`).\nYou tell it, among others, which package (VM image) will be used to run your task,\nhow much you\'d like to pay and how many providers you\'d like to involve in the execution.\nFinally, you feed it the worker script and a list of `Task` objects to execute on providers.\n\n#### Worker script\n\nThe `worker` will most likely be the very core of your requestor app. You need to define\nthis function in your agent code and then you pass it to the Executor.\n\nIt receives a `WorkContext` (`yapapi.WorkContext`) object that serves\nas an interface between your script and the execution unit within the provider.\nUsing the work context, you define the steps that the provider needs to execute in order\nto complete the job you\'re giving them - e.g. transferring files to and from the provider\nor running commands within the execution unit on the provider\'s end.\n\nDepending on the number of workers, and thus, the maximum number of providers that your\nExecutor utilizes in parallel, a single worker may tackle several tasks\n(units of your work) and you can differentiate the steps that need to happen once\nper worker run, which usually means once per provider node - but that depends on the\nexact implementation of your worker function - from those that happen for each\nindividual unit of work. An example of the former would be an upload of a source\nfile that\'s common to each fragment; and of the latter - a step that triggers the\nprocessing of the file using a set of parameters specified in the `Task` data.\n\n#### Task\n\nThe `Task` (`yapapi.Task`) object describes a unit of work that your application needs\nto carry out.\n\nThe Executor will feed an instance of your worker - bound to a single provider node -\nwith `Task` objects. The worker will be responsible for completing those tasks. Typically,\nit will turn each task into a sequence of steps to be executed in a single run\nof the execution script on a provider\'s machine, in order to compute the task\'s result.\n\n\n### Example\n\nAn example Golem application, using a Docker image containing the Blender renderer:\n\n```python\nimport asyncio\n\nfrom yapapi import Executor, Task, WorkContext\nfrom yapapi.log import enable_default_logger, log_summary, log_event_repr\nfrom yapapi.package import vm\nfrom datetime import timedelta\n\n\nasync def main(subnet_tag: str):\n    package = await vm.repo(\n        image_hash="9a3b5d67b0b27746283cb5f287c13eab1beaa12d92a9f536b747c7ae",\n        min_mem_gib=0.5,\n        min_storage_gib=2.0,\n    )\n\n    async def worker(ctx: WorkContext, tasks):\n        ctx.send_file("./scene.blend", "/golem/resource/scene.blend")\n        async for task in tasks:\n            frame = task.data\n            crops = [{"outfilebasename": "out", "borders_x": [0.0, 1.0], "borders_y": [0.0, 1.0]}]\n            ctx.send_json(\n                "/golem/work/params.json",\n                {\n                    "scene_file": "/golem/resource/scene.blend",\n                    "resolution": (400, 300),\n                    "use_compositing": False,\n                    "crops": crops,\n                    "samples": 100,\n                    "frames": [frame],\n                    "output_format": "PNG",\n                    "RESOURCES_DIR": "/golem/resources",\n                    "WORK_DIR": "/golem/work",\n                    "OUTPUT_DIR": "/golem/output",\n                },\n            )\n            ctx.run("/golem/entrypoints/run-blender.sh")\n            output_file = f"output_{frame}.png"\n            ctx.download_file(f"/golem/output/out{frame:04d}.png", output_file)\n            yield ctx.commit()\n            task.accept_result(result=output_file)\n\n        print(f"Worker {ctx.id} on {ctx.provider_name}: No more frames to render")\n\n    # iterator over the frame indices that we want to render\n    frames: range = range(0, 60, 10)\n    init_overhead: timedelta = timedelta(minutes=3)\n\n    # By passing `event_consumer=log_summary()` we enable summary logging.\n    # See the documentation of the `yapapi.log` module on how to set\n    # the level of detail and format of the logged information.\n    async with Executor(\n        package=package,\n        max_workers=3,\n        budget=10.0,\n        timeout=init_overhead + timedelta(minutes=len(frames) * 2),\n        subnet_tag=subnet_tag,\n        event_consumer=log_summary(),\n    ) as executor:\n\n        async for task in executor.submit(worker, [Task(data=frame) for frame in frames]):\n            print(f"Task computed: {task}, result: {task.result}")\n\n\nenable_default_logger()\nloop = asyncio.get_event_loop()\ntask = loop.create_task(main(subnet_tag="devnet-alpha.4"))\ntry:\n    asyncio.get_event_loop().run_until_complete(task)\nexcept (Exception, KeyboardInterrupt) as e:\n    print(e)\n    task.cancel()\n    asyncio.get_event_loop().run_until_complete(task)\n```\n',
    'author': 'Przemysław K. Rekucki',
    'author_email': 'przemyslaw.rekucki@golem.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/golemfactory/yapapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
