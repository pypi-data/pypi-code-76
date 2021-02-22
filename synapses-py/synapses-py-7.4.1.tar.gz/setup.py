# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synapses_py',
 'synapses_py.model',
 'synapses_py.model.encoding',
 'synapses_py.model.net_elems']

package_data = \
{'': ['*']}

install_requires = \
['PyFunctional>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'synapses-py',
    'version': '7.4.1',
    'description': 'A lightweight library for neural networks that runs anywhere',
    'long_description': "# Synapses\n\nA **lightweight** library for **neural networks** that **runs anywhere**!\n\n![Network Video](https://github.com/mrdimosthenis/Synapses/blob/master/network-video.gif?raw=true)\n\n## [Getting Started](https://mrdimosthenis.github.io/Synapses)\n\n### Why Sypapses?\n\n#### It's easy\n\n1. Add **one dependency** to your project.\n2. Write a **single import statement**.\n3. Use **a few pure functions**.\n\nYou are all set!\n\n#### It runs anywhere\n\nSupported languages:\n\n* [JavaScript](https://mrdimosthenis.github.io/Synapses/?javascript)\n* [Python](https://mrdimosthenis.github.io/Synapses/?python)\n* [Java](https://mrdimosthenis.github.io/Synapses/?java)\n* [C#](https://mrdimosthenis.github.io/Synapses/?csharp)\n* [Scala](https://mrdimosthenis.github.io/Synapses/?scala)\n* [F#](https://mrdimosthenis.github.io/Synapses/?fsharp)\n\n#### It's compatible across languages\n\n1. The [interface](https://github.com/mrdimosthenis/Synapses/blob/master/interface.md) is **common** across languages.\n2. You can transfer a network from one platform to another via its **json instance**.\nCreate a neural network in *Python*, train it in *Java* and get its predictions in *JavaScript*!\n\n#### It offers visualizations\n\nGet an overview of a neural network by taking a brief look at its **svg drawing**.\n\n![Network Drawing](https://github.com/mrdimosthenis/Synapses/blob/master/network-drawing.png?raw=true)\n\n#### It's customizable\n\nYou can specify the **activation function** and the **weight distribution** for the neurons of each layer.\nIf this is not enough, edit the [json instance](https://raw.githubusercontent.com/mrdimosthenis/Synapses/master/network.json) of a network to be exactly what you have in mind.\n\n#### It's efficient\n\nThe implementation is based on *lazy list*.\nThe information flows smoothly.\nEverything is obtained at a single pass.\n\n#### Data preprocessing is simple\n\nBy annotating the *discrete* and *continuous attributes*,\nyou can create a *preprocessor* that **encodes** and **decodes** the datapoints.\n\n#### Works for huge datasets\n\nThe functions that process big volumes of data, have an *Iterable/Stream* as argument.\nRAM should not get full!\n\n#### It's well tested\n\nEvery function is tested for every language.\nPlease take a look at the test projects.\n\n* [JavaScript](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/JavaScriptTest/test)\n* [Python](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/PythonTest/test)\n* [Java](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/JavaTest/src/test/java)\n* [C#](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/CSharpTest)\n* [Scala](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/ScalaTest/src/test/scala)\n* [F#](https://github.com/mrdimosthenis/Synapses/tree/master/test-projects/remote-deps/FSharpTest)\n\n### Dependencies\n\n* [circe](https://github.com/circe/circe)\n* [FSharpx.Collections](https://github.com/fsprojects/FSharpx.Collections)\n* [Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json)\n* [PyFunctional](https://github.com/EntilZha/PyFunctional)\n\n### Misc\n\n![JetBrains](https://github.com/mrdimosthenis/Synapses/blob/master/jetbrains.png?raw=true)\n\n[JetBrains tools have helped for this project!](https://www.jetbrains.com/?from=Synapses)\n",
    'author': 'Dimosthenis Michailidis',
    'author_email': 'mrdimosthenis@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mrdimosthenis.github.io/Synapses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
