# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpwebpay']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==2.8',
 'invoke>=1.4.1,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'requests==2.23',
 'tox>=3.17.1,<4.0.0']

setup_kwargs = {
    'name': 'gpwebpay',
    'version': '0.1.4',
    'description': 'GPWebPay Gateway access with Python',
    'long_description': '# gpwebpay\n![Build](https://github.com/vintesk/gpwebpay/workflows/build/badge.svg)\n![Tests](https://github.com/vintesk/gpwebpay/workflows/tests/badge.svg)\n[![codecov](https://codecov.io/gh/vintesk/gpwebpay/branch/master/graph/badge.svg)](https://codecov.io/gh/vintesk/gpwebpay)\n[![GitHub contributors](https://img.shields.io/github/contributors/vintesk/gpwebpay)](https://github.com/vintesk/gpwebpay/graphs/contributors/)\n[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-370/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://https://github.com/psf/black)\n\nGPWebPay Gateway access with Python.\n\nThis library is meant to be used by merchants that own a webshop and use GpWebPay as its payment gateway.\nAt the moment there are code examples for using GPWebPay in a webshop with PHP, where developers can see how to\nsign and verify messages exchanged with the payment gateway.\n\nWith this package you can also do it in Python and you can find an example of its usage in a webshop in the \n[demoshop repository](https://github.com/vintesk/gpwebpay_demoshop) \n\nConfiguration\n-------\n\nEnvironmental variables needed:\n```\nGPWEBPAY_MERCHANT_ID = "0987654321"     # Your merchant\'s id from gpwebpay\nGPWEBPAY_MERCHANT_PRIVATE_KEY = ""      # Your merchant\'s private key base64 encoded (cat gpwebpay-pvk.key | base64 -w0)\nGPWEBPAY_PUBLIC_KEY = ""                # GPWebPay\'s public key base64 encoded (cat gpwebpay-pub.key | base64 -w0)\nGPWEBPAY_RESPONSE_URL = ""              # The url for the callback\n```\nOptional:\n```\nGPWEBPAY_CURRENCY = "978"                       # If not set EUR is the default currency\nGPWEBPAY_DEPOSIT_FLAG = "1"                     # Requests instant payment\nGPWEBPAY_MERCHANT_PRIVATE_KEY_PASSPHRASE = ""   # If any\n```\n\nTo use this package create a GpwebpayClient:\n\n```python\nimport base64\nimport os\n\nfrom gpwebpay import gpwebpay\n\ngw = gpwebpay.GpwebpayClient()\n\n# Get your merchant\'s private key\nprivate_key = os.getenv("GPWEBPAY_MERCHANT_PRIVATE_KEY")\n# Decode your private key with base64\nprivate_key_bytes = base64.b64decode(private_key)\n\n# Call this method to request a payment to GPWebPay.\n# Returns a response, redirect to response.url to go to GPWebPay\'s and make the payment\n# The order_number needs to be unique and the amount in cents.\ngw.request_payment(order_numer="123456", amount=999, key=private_key_bytes)\n\n# Get GPWebPay\'s public key\npublic_key = os.getenv("GPWEBPAY_PUBLIC_KEY")\n# Decode it with base64\npublic_key_bytes = base64.b64decode(public_key)\n\n# Call this method to verify the response from GPWebPay\n# You need to pass here the url you received on the callback\n# Its querystring contains the data to verify the message\ngw.get_payment_result(url, key=public_key_bytes)\n```\n\nFor more details refer to the [GPWebPay documentation](https://www.gpwebpay.cz/en/Download.html)\n\n\nTests\n-------\n\nTo run the tests:\n```bash\n pytest\n ```\n\n\nDevelopment\n-------\nWe use poetry to manage dependencies, packaging and publishing.\nIf you want to develop locally [install poetry](https://python-poetry.org/docs/#installation) and run:\n\n```bash\npoetry install\n```\n',
    'author': 'Filipa Andrade',
    'author_email': 'filipa.andrade@gmail.com',
    'maintainer': 'Filipa Andrade',
    'maintainer_email': 'filipa.andrade@gmail.com',
    'url': 'https://github.com/vintesk/gpwebpay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
