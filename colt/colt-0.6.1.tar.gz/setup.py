# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'colt',
    'version': '0.6.1',
    'description': 'A configuration utility for Python object.',
    'long_description': 'colt\n===\n\n[![Actions Status](https://github.com/altescy/colt/workflows/build/badge.svg)](https://github.com/altescy/colt)\n[![Python version](https://img.shields.io/pypi/pyversions/colt)](https://github.com/altescy/colt)\n[![pypi version](https://img.shields.io/pypi/v/colt)](https://pypi.org/project/colt/)\n[![license](https://img.shields.io/github/license/altescy/colt)](https://github.com/altescy/colt/blob/master/LICENSE)\n\n## Quick Links\n\n- [Installation](#Installation)\n- [Basic Examples](Examples)\n- [kaggle Titanic Example](https://github.com/altescy/colt/tree/master/examples/titanic)\n\n## Introduction\n\n`colt` is a configuration utility for Python objects.\n`colt` constructs Python objects from a configuration dict which is convertable into JSON.\n(Inspired by [AllenNLP](https://github.com/allenai/allennlp))\n\n\n## Installation\n\n```\npip install colt\n```\n\n## Examples\n\n#### Basic Usage\n\n```python\nimport typing as tp\nimport colt\n\n@colt.register("foo")\nclass Foo:\n    def __init__(self, message: str) -> None:\n        self.message = message\n\n@colt.register("bar")\nclass Bar:\n    def __init__(self, foos: tp.List[Foo]) -> None:\n        self.foos = foos\n\nif __name__ == "__main__":\n    config = {\n        "@type": "bar",  # specify type name with `@type`\n        "foos": [\n            {"message": "hello"},  # type of this is inferred from type-hint\n            {"message": "world"},\n        ]\n    }\n\n    bar = colt.build(config)\n\n    assert isinstance(bar, Bar)\n\n    print(" ".join(foo.message for foo in bar.foos))\n        # => "hello world"\n```\n\n#### `scikit-learn` Configuration\n\n```python\nimport colt\n\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\n\nif __name__ == "__main__":\n    config = {\n        # import types automatically if type name is not registerd\n        "@type": "sklearn.ensemble.VotingClassifier",\n        "estimators": [\n            ("rfc", { "@type": "sklearn.ensemble.RandomForestClassifier",\n                      "n_estimators": 10 }),\n            ("svc", { "@type": "sklearn.svm.SVC",\n                      "gamma": "scale" }),\n        ]\n    }\n\n    X, y = load_iris(return_X_y=True)\n    X_train, X_valid, y_train, y_valid = train_test_split(X, y)\n\n    model = colt.build(config)\n    model.fit(X_train, y_train)\n\n    valid_accuracy = model.score(X_valid, y_valid)\n    print(f"valid_accuracy: {valid_accuracy}")\n```\n\n\n### `Registrable` Class\n\nBy using the `Registrable` class, you can devide namespace into each class.\nIn a following example, `Foo` and `Bar` have different namespaces.\n\n```python\nimport colt\n\nclass Foo(colt.Registrable):\n    pass\n\nclass Bar(colt.Registrable):\n    pass\n\n@Foo.register("baz")\nclass FooBaz(Foo):\n    pass\n\n@Bar.register("baz")\nclass BarBaz(Bar):\n    pass\n\n@colt.register("my_class")\nclass MyClass:\n    def __init__(self, foo: Foo, bar: Bar):\n        self.foo = foo\n        self.bar = bar\n\nif __name__ == "__main__":\n    config = {\n        "@type": "my_class",\n        "foo": {"@type": "baz"},\n        "bar": {"@type": "baz"}\n    }\n\n    obj = colt.build(config)\n\n    assert isinstance(obj.foo, FooBaz)\n    assert isinstance(obj.bar, BarBaz)\n```\n',
    'author': 'altescy',
    'author_email': 'altescy@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/altescy/colt',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
