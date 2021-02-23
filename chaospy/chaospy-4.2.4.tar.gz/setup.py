# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaospy',
 'chaospy.descriptives',
 'chaospy.descriptives.correlation',
 'chaospy.descriptives.sensitivity',
 'chaospy.distributions',
 'chaospy.distributions.baseclass',
 'chaospy.distributions.collection',
 'chaospy.distributions.copulas',
 'chaospy.distributions.kernel',
 'chaospy.distributions.operators',
 'chaospy.distributions.sampler',
 'chaospy.distributions.sampler.sequences',
 'chaospy.external',
 'chaospy.orthogonal',
 'chaospy.quadrature',
 'chaospy.quadrature.genz_keister',
 'chaospy.recurrence']

package_data = \
{'': ['*']}

install_requires = \
['numpoly', 'numpy', 'scipy']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['functools32']}

setup_kwargs = {
    'name': 'chaospy',
    'version': '4.2.4',
    'description': 'Numerical tool for perfroming uncertainty quantification',
    'long_description': '.. image:: https://github.com/jonathf/chaospy/raw/master/docs/_static/chaospy_logo.svg\n   :height: 200 px\n   :width: 200 px\n   :align: center\n\n|circleci| |codecov| |readthedocs| |downloads| |pypi| |binder|\n\n.. |circleci| image:: https://img.shields.io/circleci/build/github/jonathf/chaospy/master\n    :target: https://circleci.com/gh/jonathf/chaospy/tree/master\n.. |codecov| image:: https://img.shields.io/codecov/c/github/jonathf/chaospy\n    :target: https://codecov.io/gh/jonathf/chaospy\n.. |readthedocs| image:: https://img.shields.io/readthedocs/chaospy\n    :target: https://chaospy.readthedocs.io/en/master/?badge=master\n.. |downloads| image:: https://img.shields.io/pypi/dm/chaospy\n    :target: https://pypistats.org/packages/chaospy\n.. |pypi| image:: https://img.shields.io/pypi/v/chaospy\n    :target: https://pypi.org/project/chaospy\n.. |binder| image:: https://mybinder.org/badge_logo.svg\n    :target: https://mybinder.org/v2/gh/jonathf/chaospy/master?filepath=docs%2Ftutorials\n\nChaospy is a numerical tool for performing uncertainty quantification using\npolynomial chaos expansions and advanced Monte Carlo methods implemented in\nPython.\n\n* `Documentation <https://chaospy.readthedocs.io/en/master>`_\n* `Interactive tutorials with Binder <https://mybinder.org/v2/gh/jonathf/chaospy/master?filepath=docs%2Ftutorials>`_\n* `Source code <https://github.com/jonathf/chaospy>`_\n* `Issue tracker <https://github.com/jonathf/chaospy/issues>`_\n* `Code of Conduct <https://github.com/jonathf/chaospy/blob/master/CODE_OF_CONDUCT.md>`_\n* `Contribution Guideline <https://github.com/jonathf/chaospy/blob/master/CONTRIBUTING.md>`_\n* `Changelog <https://github.com/jonathf/chaospy/blob/master/CHANGELOg.md>`_\n\nInstallation\n------------\n\nInstallation should be straight forward using `pip <https://pypi.org/>`_:\n\n.. code-block:: bash\n\n    $ pip install chaospy\n\nFor more installation details, see the `installation guide\n<https://chaospy.readthedocs.io/en/master/installation.html>`_.\n\nExample Usage\n-------------\n\n``chaospy`` is created to work well inside numerical Python ecosystem. You\ntherefore typically need to import `Numpy <https://numpy.org/>`_ along side\n``chaospy``:\n\n.. code-block:: python\n\n    >>> import numpy\n    >>> import chaospy\n\n``chaospy`` is problem agnostic, so you can use your own code using any means\nyou find fit. The only requirement is that the output is compatible with\n`numpy.ndarray` format:\n\n.. code-block:: python\n\n    >>> coordinates = numpy.linspace(0, 10, 100)\n\n    >>> def forward_solver(coordinates, parameters):\n    ...     """Function to do uncertainty quantification on."""\n    ...     param_init, param_rate = parameters\n    ...     return param_init*numpy.e**(-param_rate*coordinates)\n\nWe here assume that ``parameters`` contains aleatory variability with known\nprobability. We formalize this probability in ``chaospy`` as a joint\nprobability distribution. For example:\n\n.. code-block:: python\n\n    >>> distribution = chaospy.J(chaospy.Uniform(1, 2), chaospy.Normal(0, 2))\n\n    >>> print(distribution)\n    J(Uniform(lower=1, upper=2), Normal(mu=0, sigma=2))\n\nMost probability distributions have an associated expansion of orthogonal\npolynomials. These can be automatically constructed:\n\n.. code-block:: python\n\n    >>> expansion = chaospy.generate_expansion(8, distribution)\n\n    >>> print(expansion[:5].round(8))\n    [1.0 q1 q0-1.5 q0*q1-1.5*q1 q0**2-3.0*q0+2.16666667]\n\nHere the polynomial is defined positional, such that ``q0`` and ``q1`` refers\nto the uniform and normal distribution respectively.\n\nThe distribution can also be used to create (pseudo-)random samples and\nlow-discrepancy sequences. For example to create Sobol sequence samples:\n\n.. code-block:: python\n\n    >>> samples = distribution.sample(1000, rule="sobol")\n\n    >>> print(samples[:, :4].round(8))\n    [[ 1.5         1.75        1.25        1.375     ]\n     [ 0.         -1.3489795   1.3489795  -0.63727873]]\n\nWe can evaluating the forward solver using these samples:\n\n.. code-block:: python\n\n    >>> evaluations = numpy.array([forward_solver(coordinates, sample)\n    ...                            for sample in samples.T])\n\n    >>> print(evaluations[:3, :5].round(8))\n    [[1.5        1.5        1.5        1.5        1.5       ]\n     [1.75       2.00546578 2.29822457 2.63372042 3.0181921 ]\n     [1.25       1.09076905 0.95182169 0.83057411 0.72477163]]\n\nHaving all these components in place, we have enough components to perform\npoint collocation. Or in other words, we can create a polynomial approximation\nof ``forward_solver``:\n\n.. code-block:: python\n\n    >>> approx_solver = chaospy.fit_regression(expansion, samples, evaluations)\n\n    >>> print(approx_solver[:2].round(4))\n    [q0 -0.0002*q0*q1**3+0.0051*q0*q1**2-0.101*q0*q1+q0]\n\nSince the model approximations are polynomials, we can do inference on them\ndirectly. For example:\n\n.. code-block:: python\n\n    >>> expected = chaospy.E(approx_solver, distribution)\n    >>> deviation = chaospy.Std(approx_solver, distribution)\n\n    >>> print(expected[:5].round(8))\n    [1.5        1.53092356 1.62757217 1.80240142 2.07915608]\n    >>> print(deviation[:5].round(8))\n    [0.28867513 0.43364958 0.76501802 1.27106355 2.07110879]\n\nFor more extensive guides on this approach an others, see the `tutorial\ncollection`_.\n\n.. _tutorial collection: https://chaospy.readthedocs.io/en/master/tutorials\n',
    'author': 'Jonathan Feinberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonathf/chaospy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
