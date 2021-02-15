# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yatl']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'pyyatl',
    'version': '0.6.0',
    'description': 'YAML Templating Language',
    'long_description': '[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)\n[![Tests](https://github.com/d5h-foss/yatl/workflows/Tests/badge.svg)](https://github.com/d5h-foss/yatl/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/d5h-foss/yatl/branch/master/graph/badge.svg)](https://codecov.io/gh/d5h-foss/yatl)\n[![PyPI](https://img.shields.io/pypi/v/pyyatl.svg)](https://pypi.org/project/pyyatl/)\n\n# Summary\n\nYATL is a templating language in which both the input and output are YAML.\nThis solves the common problem of wanting to have a template that produces YAML files,\nbut are usually solved by using an templating framework (Go templates, Jinja2, etc.), thus making the input not YAML.\nThis means you can no longer lint your input, or load it in an IDE without confusing it. It also means that your\ntemplate is probably tied to the specific language in which your toolchain is written.\n\nYATL aims to be both a standard YAML-in, YAML-out templating language, and a library to load files. This codebase\nis a Python implementation, but the plan is to make a core library with bindings for many languages.\n\nThis is a work in progress. See the [status](#Status) section below for details.\n\n# Installation\n\n```console\n$ pip install PyYATL\n```\n\n# Usage\n\n```pycon\n>>> import yatl\n>>> yatl.load("""\n... hosts:\n...     - .for (host in west_hosts):\n...         .(host)\n...     - .for (host in east_hosts):\n...         .(host)\n... """, {"west_hosts": ["west-1", "west-2"], "east_hosts": ["east-1", "east-2"]})\n{\'hosts\': [\'west-1\', \'west-2\', \'east-1\', \'east-2\']}\n```\n\n# The YATL Language\n\nThis section gives an overview of the YATL syntax. For more details, see the complete documentation (coming soon).\n\nAll YATL directives start with a `.`.\n\n## Interpolation\n\nWhen `.(p)` is seen in a value, it is replaced with the parameter value of `p`.\n\nExample:\n\n```yaml\nenvironment: .(env)\ndeployment_name: .(service_name)-.(env)\n```\n\nIf `env = production` and `service_name = foo`, then the output would be:\n\n```yaml\nenvironment: production\ndeployment_name: foo-production\n```\n\n## Conditionals\n\nExample:\n\n```yaml\ndeployment_type: canary\n.if (is_production):\n    alert-email: page_me@example.com\n```\n\nIf `is_production = true`, then the output is:\n\n```yaml\ndeployment_type: canary\nalert-email: page_me@example.com\n```\n\nYou can also have `.elif` and `.else`:\n\n```yaml\n.if (is_production):\n    slack-channel: "#production"\n.elif (is_staging):\n    slack-channel: "#staging"\n.else:\n    slack-channel: "#development"\n```\n\nYou can also use `.if` in lists. This is a special case where the value within the `.if` will extend the outer list:\n\n```yaml\nhosts:\n    - west-1\n    - west-2\n    - .if (multi_data_center):\n        - east-1\n        - east-2\n```\n\nAssuming `multi_data_center = true`, this would output:\n\n```yaml\nhosts:\n    - west-1\n    - west-2\n    - east-1\n    - east-2\n```\n\nIf you actually want a list within a list when using `.if`, you need to add an extra list wrapping the `.if`.\n\n## For Loops\n\nFor loops allow you to loop over values:\n\n```yaml\nhosts:\n    .for (host in hosts):\n        .(host)\n```\n\nIf `hosts = ["west-1", "west-2"]`, then the output would be:\n\n```yaml\nhosts:\n    - west-1\n    - west-2\n```\n\nFor loops always return lists, so the syntax is a bit loose. The following are both equivalent:\n\n```yaml\nhosts:\n    .for (host in hosts):\n        .(host)\n```\n\n```yaml\nhosts:\n    - .for (host in hosts):\n        .(host)\n```\n\n\nLike `.if`, they extend the outer list, so you can combine for loops into a single list:\n\n```yaml\nhosts:\n    - .for (host in west_hosts):\n        .(host)\n    - .for (host in east_hosts):\n        .(host)\n```\n\nAssuming the obvious assignments, this outputs:\n\n```yaml\nhosts:\n    - west-1\n    - west-2\n    - east-1\n    - east-2\n```\n\n## Loading Files\n\nYATL allows including files, to make it easier to organize large YAML objects.\n\nThe basic idea is that if you load a YATL file like this:\n\n```yaml\ntop:\n    .load_defaults_from: some-file.yaml\n    foo: bar\n```\n\nAnd `some-file.yaml` looks like this:\n\n```yaml\nbaz: quux\n```\n\nThen you\'ll get this:\n\n```yaml\ntop:\n    foo: bar\n    baz: quux\n```\n\nLoaded files can also load other files.\n\nFiles loaded with `.load_defaults_from` are always considered defaults. Hence, if a file has fields in common\nwith loaded defaults, then the file doing the loading always wins out. Otherwise objects are merged. For example,\nsay we have this in a file called `config.yaml`:\n\n```yaml\nouter:\n    .load_defaults_from: some-file.yaml\n    inner:\n        foo: bar\n```\n\nIf `some-file.yaml` looks like this:\n\n```yaml\ninner:\n    foo: baz\n```\n\nThen the result will be this (fields in both `config.yaml` and `some-file.yaml` are taken from `config.yaml`, because\nloads are always defaults):\n\n```yaml\nouter:\n    inner:\n        foo: bar\n```\n\nIf `some-file.yaml` looks like this instead:\n\n```yaml\ninner:\n    baz: quux\n```\n\nThen the result would be this (fields in objects are merged):\n\n```yaml\nouter:\n    inner:\n        foo: bar\n        baz: quux\n```\n\nIf `inner` was not an object (e.g., it\'s a list) in either file, then no merging will happen, and whatever is in\n`config.yaml` will be the result.\n\nLastly, if a file loads two or more files which both have defaults for the same field, then whichever is loaded at\nthe highest nesting level will win. For example, if we have:\n\n```yaml\nouter:\n    .load_defaults_from: file1.yaml\n    inner:\n        load_defaults_from: file2.yaml\n```\n\nIf both `file1.yaml` and `file2.yaml` have defaults for the same field (which would have to be inside `inner`), then the\ndefaults from `file2.yaml` will take precendence.\n\n## Definitions\n\nDefinitions in YATL are an improvement over anchors in YAML. They\'re a bit like a function:\n\n```yaml\n.def email_on_failure(email):\n    .if (is_production):\n        on-failure:\n            alert-email: .(email)\ntasks:\n    - test:\n        command: run_tests.sh\n        .use email_on_failure: tests@example.com\n    - deploy:\n        command: do_deploy.sh\n        .use email_on_failure: deploys@example.com\n```\n\nIf `is_production = true`, then the output will be:\n\n```yaml\ntasks:\n    - test:\n        command: run_tests.sh\n        on-failure:\n            alert-email: tests@example.com\n    - deploy:\n        command: do_deploy.sh\n        on-failure:\n            alert-email: deploys@example.com\n```\n\nIf `is_production = false` then the `on-failure` parts will be left out.\n\nDefinitions are more powerful than anchors because you can parameterize them.\nThey\'re also cleaner because, unlike anchors, the definition doesn\'t remain in the output.\nOnly the usages are in the output.\n\nDefinitions can have zero to any number of arguments. If they have zero arguments, then\npass an empty string, list, or object as the argument when using it (this is just so the syntax is valid YAML):\n\n```yaml\n.def replicas:\n    .if (is_production): 3\n    .else: 1\n\nservices:\n    .for (s in services):\n        name: .(s)\n        replicas:\n            .use replicas: {}\n```\n\nIf `is_production = true` and `services = ["foo", "bar"]`, then the output will be:\n\n```yaml\nservices:\n    - name: foo\n      replicas: 3\n    - name: bar\n      replicas: 3\n```\n\nIf there are multiple arguments, they can be passed as an object or list:\n\n```yaml\n.def task(name, command):\n    name: .(name)\n    command: .(command)\n    container: ubuntu\n    .if (is_production):\n        on-failure:\n            alert-email: errors@example.com\n\ntasks:\n    - .use task:  # Pass args as an object\n        name: build\n        command: build.sh\n    - .use task:  # Pass args as a list\n        - test\n        - test.sh\n    - .use task: [deploy, deploy.sh]  # Shorthand list\n```\n\nIf `is_production = false`, the output will be:\n\n```yaml\ntasks:\n    - name: build\n      command: build.sh\n      container: ubuntu\n    - name: test\n      command: test.sh\n      container: ubuntu\n    - name: deploy\n      command: deploy.sh\n      container: ubuntu\n```\n\n# Status\n\n⚠️ The language spec is likely to change at least slightly.\n\n- [x] Proof of concept\n- [ ] Support safe expressions\n- [ ] Polish (load lists of files, allow escaping, etc.)\n- [ ] Complete documentation\n- [ ] Include line number with error messages and don\'t stop at the first error\n- [ ] Support Python versions other than CPython 3.6 and Python 3.7+ (because of dict ordering)\n\nThis software should be considered beta.\n',
    'author': 'Dan Hipschman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d5h-foss/yatl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
