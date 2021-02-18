# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thorbanks', 'thorbanks_models']

package_data = \
{'': ['*'], 'thorbanks': ['static/img/payment/*', 'templates/thorbanks/*']}

install_requires = \
['Django>=1.11.27', 'cryptography>=2']

setup_kwargs = {
    'name': 'django-thorbanks',
    'version': '0.6.2',
    'description': '`django-thorbanks` provides a Django application for Estonian banklinks (iPizza protocol).',
    'long_description': '# django-thorbanks\n\n[![Build Status](https://travis-ci.org/thorgate/django-thorbanks.svg?branch=master)](https://travis-ci.org/thorgate/django-thorbanks)\n[![Coverage Status](https://coveralls.io/repos/github/thorgate/django-thorbanks/badge.svg?branch=master)](https://coveralls.io/github/thorgate/django-thorbanks?branch=master)\n[![PyPI release](https://badge.fury.io/py/django-thorbanks.png)](https://badge.fury.io/py/django-thorbanks)\n\n\nDjango app for integrating Estonian banklinks into your project.\n\n## Features\n\nBank            | Protocol    | Authentication      | Payment\n--------------- | ----------- | ------------------- | -------\nSwedbank        | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\nSEB             | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\nDanske          | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\nLHV             | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\nKrediidipank    | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\nNordea          | iPizza      | :heavy_check_mark:  | :heavy_check_mark:\n\n## Usage\n\n### 1. Install it:\n\n**Pip:**\n\n```bash\npip install django-thorbanks\n```\n\n**Pipenv:**\n\n```bash\npipenv install django-thorbanks\n```\n\n**Poetry:**\n\n```bash\npoetry add django-thorbanks\n```\n\n### 2. Add to installed apps\n\n```python\nINSTALLED_APPS = (\n    # Add the following apps:\n    "thorbanks",\n    "thorbanks_models",\n)\n```\n\n### 3. Configure and create migrations:\n\n**With MANUAL_MODELS:**\n\n- Remove `"thorbanks_models"` from `INSTALLED_APPS`\n- follow instructions from [thorbanks.settings.get_model](./thorbanks/settings.py#L59).\n\n**With default models:**\n\nMake django aware that thorbanks migrations are in your local apps folder via settings.MIGRATION_MODULES:\n\n> Note: Replace `shop` with the name of an existing app in your project.\n\n```python\n# Tell django that thorbanks_models migrations are in shop app (in thorbanks_migrations module)\nMIGRATION_MODULES = {"thorbanks_models": "shop.thorbanks_migrations"}\n```\n\nNow run `makemigrations thorbanks_models` and `migrate` management commands to create and apply the migrations.\n\n### 4. Add settings.BANKLINKS\n\nFor a working example see the definitions in [example/settings.py](example/settings.py).\n\n> Note:\n>You will need a public and private key for each bank integration.\n>In case you don\'t have the public key, you can generate one out of a certificate by:\n>```\n>openssl x509 -pubkey -noout -in cert.pem  > pubkey.pem\n>```\n\n### 5. Link Transaction to your Order model\n\n> Note: When using MANUAL_MODELS replace `thorbanks_models` with your local app name\n\n```python\nclass Order(models.Model):\n    # ... other fields\n    transaction = models.OneToOneField(\n        "thorbanks_models.Transaction", null=True, on_delete=models.SET_NULL\n    )\n```\n\n### 6. Include thorbanks urls\n\n```python\nurlpatterns = [\n    # This is where the user will be redirected after returning from the banklink page\n    url(r"^banks/", include("thorbanks.urls")),\n]\n```\n\n### 7. Add listeners to banklinks success & failure callbacks:\n\nSee [example.shop.models.banklink_success_callback](example/shop/models.py#L23) and [example.shop.models.banklink_failed_callback](example/shop/models.py#L44).\n\n### 8. Create views and forms for payments:\n\nsee [example.shop.views](example/shop/views.py) and [example.shop.forms](example/shop/forms.py).\n\n## iPizza protocol\n\n- [Test service](https://banks.maximum.thorgate.eu/et/info)\n- [Swedbank](https://www.swedbank.ee/business/cash/ecommerce/ecommerce?language=EST)\n    - [Spec](https://www.swedbank.ee/static/pdf/business/d2d/paymentcollection/Pangalingi_paringute_tehniline_spetsifikatsioon_09_10_2014.pdf)\n- [SEB](https://www.seb.ee/ariklient/igapaevapangandus/maksete-kogumine/maksete-kogumine-internetis/pangalingi-tehniline)\n- [LHV Bank](https://www.lhv.ee/pangateenused/pangalink/)\n',
    'author': 'Thorgate',
    'author_email': 'info@thorgate.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://thorgate.eu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
