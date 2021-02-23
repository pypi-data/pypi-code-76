# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magicapi',
 'magicapi.Decorators',
 'magicapi.Errors',
 'magicapi.FieldTypes',
 'magicapi.Globals',
 'magicapi.Models',
 'magicapi.RouteClasses',
 'magicapi.Services',
 'magicapi.Services.Doorman',
 'magicapi.Services.Email',
 'magicapi.Services.MagicLink',
 'magicapi.Services.Mailgun',
 'magicapi.Services.Segment',
 'magicapi.Services.Sentry',
 'magicapi.Services.Stripe',
 'magicapi.Services.Twilio',
 'magicapi.Utils']

package_data = \
{'': ['*']}

install_requires = \
['analytics-python>=1.2.9,<2.0.0',
 'boto3>=1.14.23,<2.0.0',
 'fastapi[all]>=0.63.0,<0.64.0',
 'magicdb>=0.2.139,<0.3.0',
 'mangum>=0.9.2,<0.10.0',
 'phonenumbers>=8.12.6,<9.0.0',
 'pydantic[dotenv]>=1.7.3,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'sentry-sdk>=0.19.4,<0.20.0',
 'stripe>=2.49.0,<3.0.0',
 'twilio>=6.44.0,<7.0.0',
 'typer>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['magic = magicapi.cli:app']}

setup_kwargs = {
    'name': 'magicapi',
    'version': '0.1.142',
    'description': '',
    'long_description': '# Magic API\n\nThe Magic API!\n\n1) incr the toml version\n2) poetry publish --build\n\n\nFor CLI:\n# Magic CLI (magicapi has this built in)\n\nThe best server maker.\n\nSteps:\n\n1) pip install magicapi (make sure the pip points to the correct python (3.6+))\n\n2) cd into the directory you want the server to be in\n\n// use the cli to create the app\n\n3) magic create < app name >\n\n4) cd < app name >\n\n// now make the virtual env and pip install the requirements\n5) python3 -m venv venv\n\n6) source venv/bin/activate\n\n7) `pip install -r requirements.txt`\n8) `pip install --upgrade magicdb magicapi`\n\n// files needed to run\n8) Create an .env file in the < app name > directory.\n\na) Use the ".example_env" as a template. Fill in the env variables for the services you will need to use.\n\nb) The SERVICE and TASKS_TABLE_NAME are required for the app.\n\n// add firestore\n1) add the firestore service account json to the < app name > and name it "my-service-account.json"\n\n// to deploy to aws lambda\n\n1) Create a user on AWS and sign in via the CLI (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)\n \n2) npm i\n\n2) magic deploy\n\nThat should be it for the setup!\n\nTime to run it!\n\nTo start a local server: magic start\n\nTo test local server (while local server is running): magic test\n\nTo deploy for the first time or any time you change the serverless yaml: magic deploy\n\nTo deploy when you just edited the app code: magic deploy_again\n\nTo update magicapi:\npip install --upgrade magicapi\n',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jerber/MagicAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
