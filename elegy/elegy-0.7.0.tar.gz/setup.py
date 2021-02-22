# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elegy',
 'elegy.callbacks',
 'elegy.data',
 'elegy.generalized_module',
 'elegy.generalized_optimizer',
 'elegy.losses',
 'elegy.metrics',
 'elegy.model',
 'elegy.nets',
 'elegy.nn',
 'elegy.regularizers']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.5.0,<2.0.0',
 'dm-haiku>=0.0.2,<0.0.3',
 'jax>=0.2.9,<0.3.0',
 'jaxlib>=0.1.59,<0.2.0',
 'numpy>=1.0.0,<2.0.0',
 'optax>=0.0.1,<0.0.2',
 'pyyaml>=5.3.1,<6.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tensorboardx>=2.1,<3.0',
 'toolz>=0.10.0,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'elegy',
    'version': '0.7.0',
    'description': 'Elegy is a Neural Networks framework based on Jax and Haiku.',
    'long_description': '# Elegy\n[![PyPI Status Badge](https://badge.fury.io/py/elegy.svg)](https://pypi.org/project/elegy/)\n[![Coverage](https://img.shields.io/codecov/c/github/poets-ai/elegy?color=%2334D058)](https://codecov.io/gh/poets-ai/elegy)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/elegy)](https://pypi.org/project/elegy/)\n[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://poets-ai.github.io/elegy/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/poets-ai/elegy/issues)\n[![Status](https://github.com/poets-ai/elegy/workflows/GitHub%20CI/badge.svg)](https://github.com/poets-ai/elegy/actions?query=workflow%3A"GitHub+CI")\n\n-----------------\n\n_Elegy is a framework-agnostic Trainer interface for the Jax ecosystem._  \n\n#### Main Features\n* **Easy-to-use**: Elegy provides a Keras-like high-level API that makes it very easy to do common tasks.\n* **Flexible**: Elegy provides a functional Pytorch Lightning-like low-level API that provides maximal flexibility when needed.\n* **Agnostic**: Elegy supports a variety of frameworks including Flax, Haiku, and Optax on the high-level API, and it is 100% framework-agnostic on the low-level API.\n* **Compatible**: Elegy can consume a wide variety of common data sources including TensorFlow Datasets, Pytorch DataLoaders, Python generators, and Numpy pytrees.\n\nFor more information take a look at the [Documentation](https://poets-ai.github.io/elegy).\n\n## Installation\n\nInstall Elegy using pip:\n```bash\npip install elegy\n```\n\nFor Windows users we recommend the Windows subsystem for linux 2 [WSL2](https://docs.microsoft.com/es-es/windows/wsl/install-win10?redirectedfrom=MSDN) since [jax](https://github.com/google/jax/issues/438) does not support it yet.\n\n## Quick Start: High-level API\nElegy\'s high-level API provides a very simple interface you can use by implementing following steps:\n\n**1.** Define the architecture inside a `Module`. We will use Flax Linen for this example:\n```python\nimport flax.linen as nn\nimport jax\n\nclass MLP(nn.Module):\n    @nn.compact\n    def call(self, x):\n        x = nn.Dense(300)(x)\n        x = jax.nn.relu(x)\n        x = nn.Dense(10)(x)\n        return x\n```\n\n**2.** Create a `Model` from this module and specify additional things like losses, metrics, and optimizers:\n```python\nimport elegy, optax\n\nmodel = elegy.Model(\n    module=MLP(),\n    loss=[\n        elegy.losses.SparseCategoricalCrossentropy(from_logits=True),\n        elegy.regularizers.GlobalL2(l=1e-5),\n    ],\n    metrics=elegy.metrics.SparseCategoricalAccuracy(),\n    optimizer=optax.rmsprop(1e-3),\n)\n```\n**3.** Train the model using the `fit` method:\n```python\nmodel.fit(\n    x=X_train,\n    y=y_train,\n    epochs=100,\n    steps_per_epoch=200,\n    batch_size=64,\n    validation_data=(X_test, y_test),\n    shuffle=True,\n    callbacks=[elegy.callbacks.TensorBoard("summaries")]\n)\n```\n\n## Quick Start: Low-level API\nIn Elegy\'s low-level API lets you define exactly what goes on during training, testing, and inference. Lets define the `test_step` to implement a linear classifier in pure jax:\n\n**1.** Calculate our loss, logs, and states:\n```python\nclass LinearClassifier(elegy.Model):\n    # request parameters by name via depending injection.\n    # names: x, y_true, sample_weight, class_weight, states, initializing\n    def test_step(\n        self,\n        x, # inputs\n        y_true, # labels\n        states: elegy.States, # model state\n        initializing: bool, # if True we should initialize our parameters\n    ):  \n        rng: elegy.RNGSeq = states.rng\n        # flatten + scale\n        x = jnp.reshape(x, (x.shape[0], -1)) / 255\n        # initialize or use existing parameters\n        if initializing:\n            w = jax.random.uniform(\n                rng.next(), shape=[np.prod(x.shape[1:]), 10]\n            )\n            b = jax.random.uniform(rng.next(), shape=[1])\n        else:\n            w, b = states.net_params\n        # model\n        logits = jnp.dot(x, w) + b\n        # categorical crossentropy loss\n        labels = jax.nn.one_hot(y_true, 10)\n        loss = jnp.mean(-jnp.sum(labels * jax.nn.log_softmax(logits), axis=-1))\n        accuracy=jnp.mean(jnp.argmax(logits, axis=-1) == y_true)\n        # metrics\n        logs = dict(\n            accuracy=accuracy,\n            loss=loss,\n        )\n        return loss, logs, states.update(net_params=(w, b))\n```\n\n**2.** Instantiate our `LinearClassifier` with an optimizer:\n```python\nmodel = LinearClassifier(\n    optimizer=optax.rmsprop(1e-3),\n)\n```\n**3.** Train the model using the `fit` method:\n```python\nmodel.fit(\n    x=X_train,\n    y=y_train,\n    epochs=100,\n    steps_per_epoch=200,\n    batch_size=64,\n    validation_data=(X_test, y_test),\n    shuffle=True,\n    callbacks=[elegy.callbacks.TensorBoard("summaries")]\n)\n```\n#### Using Jax Frameworks\nIt is straightforward to integrate other functional JAX libraries with this \nlow-level API:\n\n```python\nclass LinearClassifier(elegy.Model):\n    def test_step(\n        self, x, y_true, states: elegy.States, initializing: bool\n    ):\n        rng: elegy.RNGSeq = states.rng\n        x = jnp.reshape(x, (x.shape[0], -1)) / 255\n        if initializing:\n            logits, variables = self.module.init_with_output(\n                {"params": rng.next(), "dropout": rng.next()}, x\n            )\n        else:\n            variables = dict(params=states.net_params, **states.net_states)\n            logits, variables = self.module.apply(\n                variables, x, rngs={"dropout": rng.next()}, mutable=True\n            )\n        net_states, net_params = variables.pop("params")\n        \n        labels = jax.nn.one_hot(y_true, 10)\n        loss = jnp.mean(-jnp.sum(labels * jax.nn.log_softmax(logits), axis=-1))\n        accuracy = jnp.mean(jnp.argmax(logits, axis=-1) == y_true)\n\n        logs = dict(accuracy=accuracy, loss=loss)\n        return loss, logs, states.update(net_params=net_params, net_states=net_states)\n```\n\n## More Info\n* [Getting Started: High-level API](https://poets-ai.github.io/elegy/getting-started-high-level-api/) tutorial.\n* [Getting Started: Low-level API](https://poets-ai.github.io/elegy/getting-started-low-level-api/) tutorial.\n* Elegy\'s [Documentation](https://poets-ai.github.io/elegy).\n* The [examples](https://github.com/poets-ai/elegy/tree/master/examples) directory.\n* [What is Jax?](https://github.com/google/jax#what-is-jax)\n\n### Examples\nTo run the examples first install some required packages:\n```\npip install -r examples/requirements.txt\n```\nNow run the example:\n```\npython examples/flax_mnist_vae.py \n```\n\n## Contributing\nDeep Learning is evolving at an incredible pace, there is so much to do and so few hands. If you wish to contribute anything from a loss or metric to a new awesome feature for Elegy just open an issue or send a PR! For more information check out our [Contributing Guide](https://poets-ai.github.io/elegy/guides/contributing).\n\n## About Us\nWe are some friends passionate about ML.\n\n## License\nApache\n\n## Citing Elegy\n\nTo cite this project:\n\n**BibTeX**\n\n```\n@software{elegy2020repository,\nauthor = {PoetsAI},\ntitle = {Elegy: A framework-agnostic Trainer interface for the Jax ecosystem},\nurl = {https://github.com/poets-ai/elegy},\nversion = {0.7.0},\nyear = {2020},\n}\n```\n\n\nWhere the current *version* may be retrieved either from the `Release` tag or the file [elegy/\\_\\_init\\_\\_.py](https://github.com/poets-ai/elegy/blob/master/elegy/__init__.py) and the *year* corresponds to the project\'s release year.\n',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://poets-ai.github.io/elegy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.9',
}


setup(**setup_kwargs)
