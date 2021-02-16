# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_iconify']

package_data = \
{'': ['*']}

install_requires = \
['Django>2.1,<4.0']

setup_kwargs = {
    'name': 'django-iconify',
    'version': '0.1.0',
    'description': 'Iconify API implementation and tools for Django projects',
    'long_description': 'Iconify API implementation and tools for Django projects\n========================================================\n\nThis re-usable app hepls integrating `Iconify`_ into Django projects.\nIconify is a unified icons framework, providing access to 40,000+ icons\nfrom different icon sets.\n\nIconify replaces classical icon fonts, claiming that such fonts would\nget too large for some icon sets out there. Instead, it provides an API\nto add icons in SVG format from its collections.\n\n`django-iconify`_ eases integration into Django. Iconify, to be performant,\nuses a server-side API to request icons from (in batches, with transformations\napplied, etc.). Upstream provides a CDN-served central API as well as\nself-hosted options written in PHP or Node.js, all of which are undesirable\nfor Django projects. `django-iconify`_ implements the Iconify API as a\nre-usable Django app.\n\nInstallation\n------------\n\nTo add `django-iconify`_ to a project, first add it as dependency to your\nproject, e.g. using `poetry`_::\n\n  $ poetry add django-iconify\n\nThen, add it to your `INSTALLED_APPS` setting to make its views available\nlater::\n\n  INSTALLED_APPS = [\n      ...\n      "dj_iconify.apps.DjIconifyConfig",\n      ...\n  ]\n\nYou need to make the `JSON collection`_ available by some means. You can\ndownload it manually, or use your favourite asset management library. For\ninstance, you could use `django-yarnpkg`_ to depend on the `@iconify/json`\nYarn package::\n\n  YARN_INSTALLED_APPS = [\n    "@iconify/json",\n  ]\n  NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")\n\nNo matter which way, finally, you have to configure the path to the\ncollections in your settings::\n  \n  ICONIFY_JSON_ROOT = os.path.join(NODE_MODULES_ROOT, "@iconify", "json")\n\nIf you do not use `django-yarnpkg`_, construct the path manually, ot use\nwhatever mechanism your asset manager provides.\n\nFinally, include the URLs in your `urlpatterns`::\n\n  from django.urls import include, path\n\n  urlpatterns = [\n      path("icons/", include("dj_iconify.urls")),\n  ]\n\nUsage\n-----\n\nIconify SVG Framework\n~~~~~~~~~~~~~~~~~~~~~\n\nTo use the `Iconify SVG Framework`_, get its JavaScript from somewhere\n(e.g. using `django-yarnpkg`_ again, or directly from the CDN, from your\now nstatic files, or wherever).\n\n`django-iconify`_ provides a view that returns a small JavaScript snippet\nthat configures the `Iconify SVG Framework`_ to use its API endpoints. In\nthe following example, we first load this configuration snippet, then\ninclude the `Iconify SVG Framework`_ from the CDN (do not do this in\nproduction, where data protection matters)::\n\n  <script type="text/javascript" src="{% url \'config.js\' %}"></script>\n  <script type="text/javascript" src="https://code.iconify.design/1/1.0.6/iconify.min.js"></script>\n\nLoading SVG directly ("How to use Iconify in CSS")\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n`django-iconify`_ also implements the direct SVG API. For now, you have to use\nDjango\'s regular URL reverse resolver to construct an SVG URL, or craft it\nby hand::\n\n  <img src="{% url \'iconify_svg\' \'mdi\' \'account\' %}?rotate=90deg %}" />\n\nDocumentation on what query parameters are supported can be found in the\ndocumentation on `How to use Iconify in CSS`_.\n\nIn the future, a template tag will be available to simplify this.\n\nIncluding SVG in template directly\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n*Not implemented yet*\n\nIn the future, a template tag will be available to render SVG icons directly\ninto the template, which can be helpful in situations where retrieving external\nresources in undesirable, like HTML e-mails.\n\nExample\n-------\n\nThe source distribution as well as the `Git repository` contain a full example\napplication that serves the API under `/icons/` and a test page under `/test.html`.\n\nIt is reduced to a minimal working example for the reader\'s convenience.\n\n_`Iconify`: https://iconify.design/\n_`django-iconify`: https://edugit.org/AlekSIS/libs/django-iconify\n_`poetry`: https://python-poetry.org/\n_`JSON collection`: https://github.com/iconify/collections-json\n_`django-yarnpkg`: https://edugit.org/AlekSIS/libs/django-yarnpkg\n_`Iconify SVG Framework`: https://docs.iconify.design/implementations/svg-framework/\n_`How to use Iconify in CSS`: https://docs.iconify.design/implementations/css.html\n_`Git repository`: https://edugit.org/AlekSIS/libs/django-iconify\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/django-iconify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
