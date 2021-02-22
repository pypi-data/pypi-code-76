# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_hypermodel']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-hypermodel',
    'version': '0.1.0',
    'description': 'A FastAPI + Pydantic extension for simplifying hypermedia-driven API development.',
    'long_description': '# FastAPI-HyperModel\n\nFastAPI-HyperModel is a FastAPI + Pydantic extension for simplifying hypermedia-driven API development. This module adds a new Pydantic model base-class, supporting dynamic `href` generation based on object data.\n\n## Installation\n\n`pip install fastapi-hypermodel`\n\n## Basic Usage\n\n### Import `HyperModel` and optionally `HyperRef`\n\n```python\nfrom fastapi import FastAPI\n\nfrom fastapi_hypermodel import HyperModel, HyperRef\n```\n\n`HyperModel` will be your model base-class, and `HyperRef` is just a type alias for `Optional[pydantic.AnyUrl]`\n\n### Create your basic models\n\nWe\'ll create two models, a brief item summary including ID, name, and a link, and a full model containing additional information. We\'ll use `ItemSummary` in our item list, and `ItemDetail` for full item information.\n\n```python\nclass ItemSummary(HyperModel):\n    id: str\n    name: str\n    href: HyperRef\n\nclass ItemDetail(ItemSummary):\n    description: Optional[str] = None\n    price: float\n```\n\n### Create and attach your app\n\nWe\'ll now create our FastAPI app, and bind it to our `HyperModel` base class.\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\nHyperModel.init_app(app)\n```\n\n### Add some API views\n\nWe\'ll create an API view for a list of items, as well as details about an individual item. Note that we pass the item ID with our `{item_id}` URL variable.\n\n```python\n@app.get("/items", response_model=List[ItemSummary])\ndef read_items():\n    return list(items.values())\n\n\n@app.get("/items/{item_id}", response_model=ItemDetail)\ndef read_item(item_id: str):\n    return items[item_id]\n```\n\n### Configure our model Hrefs\n\nWe\'ll now go back and add a special configuration class to our models. This class defines how our href elements will be generated. We\'ll change our `ItemSummary` class to:\n\n```python\nclass ItemSummary(HyperModel):\n    id: str\n    name: str\n    href: HyperRef\n\n    class Href:\n        endpoint = "read_item"  # FastAPI endpoint we want to link to\n        field = "href"  # Which field should hold our URL\n        values = {"item_id": "<id>"}  # Map object attributes to URL variables\n```\n\nWe need to create a child class named `Href` containing three important attributes:\n\n#### `endpoint`\n\nName of your FastAPI endpoint function you want to link to. In our example, we want our item summary to link to the corresponding item detail page, which maps to our `read_item` function.\n\n#### `field` (optional)\n\nDetermines which field the generated URL should be assigned to. This is an optional property and will default to "href". Note, if the selected field is not defined by your schema, the link will not be generated.\n\n#### `values` (optional depending on endpoint)\n\nSame keyword arguments as FastAPI\'s url_path_for, except string arguments enclosed in < > will be interpreted as attributes to pull from the object. For example, here we need to pass an `item_id` argument as required by our endpoint function, and we want to populate that with our item object\'s `id` attribute.\n\n### Putting it all together\n\nFor this example, we can make a dictionary containing some fake data, and add extra models, even nesting models if we want. A complete example based on this documentation can be found [here](examples/simple_app.py).\n\nIf we run the example application and go to our `/items` URL, we should get a response like:\n\n```json\n[\n  {\n    "name": "Foo",\n    "id": "item01",\n    "href": "/items/item01"\n  },\n  {\n    "name": "Bar",\n    "id": "item02",\n    "href": "/items/item02"\n  },\n  {\n    "name": "Baz",\n    "id": "item03",\n    "href": "/items/item03"\n  }\n]\n```\n\n## Attributions\n\nSome functionality is based on [Flask-Marshmallow](https://github.com/marshmallow-code/flask-marshmallow/blob/dev/src/flask_marshmallow/fields.py) `URLFor` class.\n\n## To-do\n\n- [ ] Proper unit tests\n',
    'author': 'Joel Collins',
    'author_email': 'joel.collins@renalregistry.nhs.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtc42/fastapi-hypermodel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
