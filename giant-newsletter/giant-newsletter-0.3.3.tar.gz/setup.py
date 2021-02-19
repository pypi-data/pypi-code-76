# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newsletter', 'newsletter.migrations', 'newsletter.tests']

package_data = \
{'': ['*'], 'newsletter': ['templates/*', 'templates/newsletter/*']}

install_requires = \
['giant-mixins']

setup_kwargs = {
    'name': 'giant-newsletter',
    'version': '0.3.3',
    'description': 'A small reusable package that adds a Newsletter app to a project',
    'long_description': '# Giant Newsletter\n\nA re-usable package which can be used in any project that requires a generic `Newletter` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin and email sending.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-newsletter\n\nYou should then add `"newsletter"` to the `INSTALLED_APPS` in your settings file and to the `Makefile`.  \n\nIn `base.py` there should also be a `DEFAULT_FROM_EMAIL` and a `DEFAULT_TO_EMAIL`. This is used by the email sending method.\n\n ## Context Processor\n If you wish to use the Contact form with the context processor you will need to add `newsletter.context_processors.subscription_form` into the `TEMPLATES` context processors list. This will allow you to access the form in templates.\n \n ## Configuration\n\n- `NEWSLETTER_FORM_FIELDS` allows the user to customise what fields are displayed on the form. This must be a list\n- `NEWSLETTER_FORM_FIELD_PLACEHOLDERS` allows the user to customise the field placeholder text. This must be a dict containing the fieldnames\n- `NEWSLETTER_FORM_REQUIRED_FIELDS` allows the user to customise what fields are required on the form. This must be a list\n- `NEWSLETTER_FORM_LABELS` allows the user to customise what the field labels are on the form. This must be a dict of field names and their corresponding label\n- `NEWSLETTER_FORM_WIDGETS` allows the user to customise what the field widgets are on the form. This must be a dict of field names and their corresponding widget\n- `NEWSLETTER_HTTP_REFERER` allows the user to customise the success url and return the user to the referer page after submission',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-newsletter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
