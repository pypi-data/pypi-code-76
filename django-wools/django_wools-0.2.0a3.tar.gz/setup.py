# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_wools', 'django_wools.templatetags']

package_data = \
{'': ['*'], 'django_wools': ['templates/wools/images/*']}

install_requires = \
['django>1.7.0', 'psutil>2.0.0', 'tqdm>3.0.0', 'zopflipy>1.1']

setup_kwargs = {
    'name': 'django-wools',
    'version': '0.2.0a3',
    'description': 'Django tools from WITH',
    'long_description': 'Django Wools\n============\n\nDjango tools from WITH.\n\nThat\'s a collection of things that we at [WITH](https://with-madrid.com/) got\ntired of copy/pasting in every project.\n\n## Install\n\n```\npip install django_wools\n```\n\n## Included Wools\n\n### Storage\n\n#### `django_wools.storage.GzipManifestStaticFilesStorage`\n\nThat\'s a sub-class of the \n[ManifestStaticFilesStorage](https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage)\nbut that makes sure that along with all the files comes a `.gz` version which\nis easy to pick up for nginx (or other static files server).\n\n### Middlewares\n\n#### `django_wools.middlewares.NowMiddleware`\n\nSuppose that you have a content that is available up until a given date. When\nthe date is passed then everything related to this content expires. However,\nin order to do this, you\'re probably going to make several request, possibly in\nloosely connected parts of your code. In those cases, when looking at the time,\nthe clock will show different value as the time passes between calls. It means\nthat you could very well end up with one half of your code considering that the\nobject is still valid but the other half that it expired.\n\nIn order to prevent this, the simplest is to consider that the time is fixed\nand that the code executes instantly at the moment of the request. The goal\nof this middleware is to save the current time at each request and then to\nprovide an easy way to get the current time through the request.\n\nIf the middleware is activated, you should be able to get the time like this:\n\n```python\nfrom time import sleep\nfrom django.shortcuts import render\n\ndef my_view(request):\n    print(f"Now is {request.now()}")\n    sleep(42)\n    print(f"Now is still {request.now()}")\n\n    return render(request, "something.html", {"now": request.now()})\n```\n\n#### `django_wools.middlewares.SlowMiddleware`\n\nWhen developing a SPA or hybrid app, you want to make sure that the app is\nstructurally ready to handle load times from the server, even if the connection\nis a bit shaky. Also, you want to make sure that not too many requests are\nsent.\n\nIn order for you to fully realize how slow your website is going to be on a bad\nconnection, th e SlowMiddleware will automatically add a delay before replying\nto each request.\n\nAdd this to your `settings.py`\n\n```python\nMIDDLEWARE = [\n    # ...\n    "django_wools.middlewares.SlowMiddleware",\n]\n\nSLOW_MIDDLEWARE_LATENCY = 1 if DEBUG else 0\n```\n\nBy doing this, your requests will be added a 1s delay if the `DEBUG` mode is\nenabled.\n\n### Database\n\n#### `django_wools.db.require_lock`\n\nProvides a way to explicitly generate a PostgreSQL lock on a table.\n\nBy example:\n\n```python\nfrom django.db.transaction import atomic\nfrom django_wools.db import require_lock\n\nfrom my_app.models import MyModel\n\n\n@atomic\n@require_lock(MyModel, \'ACCESS EXCLUSIVE\')\ndef myview(request):\n    # do stuff here\n```\n\n### Wagtail Images\n\nSeveral Wagtail-specific tags are provided to deal with images and more\nspecifically responsive images. To use it:\n\n1. Add `django_wools` to `INSTALLED_APPS`\n2. Import `wools_for_wt_images` from your template\n\n```\n{% load wools_for_wt_images %}\n```\n\nSome specific settings can be set:\n\n- `WOOLS_MAX_PIXEL_RATIO` _(default: `3`)_ &mdash; Highest device pixel ratio\n  to support.\n- `WOOLS_INCREMENT_STEP_PERCENT` _(default: `(sqrt(2) - 1) * 100`)_ &mdash; The\n  percentage of increase from the base density to the next one. The default\n  values will generate `x1`, `x2` and `x4` with intermediate values that are\n  `x1.4142` and `x2.8284`.\n\nAll the tags will be default generate WebP images with a PNG fallback. The\nfallback can be changed to JPEG and the main format has to be WebP.\n\n#### `image_fixed_size`\n\nThis tag will generate a `<picture>` tag for an image whose size in pixels you\nknown in advance. That picture size will be enforced in the HTML code with\ninline properties.\n\nUsage:\n\n```\n{% image_fixed_size max-500x500 %}\n```\n\nThe arguments to this tag, in order, are:\n\n- `image` &mdash; The Wagtail-compatible image itself\n- `spec` &mdash; A spec like you would give to Wagtail (`fill-500x500`,\n   `max-500x500`, etc)\n- `fallback_format` &mdash; The format to fallback in case the browser doesn\'t\n  support WebP. Can either be `"jpeg"` or `"png"`. Defaults to `"png"`.\n- `lossless` &mdash; A boolean to enable losslessness of WebP. This does not\n  affect the fallback format, so if you want a lossless fallback as well you\'ll\n  need to use PNG.\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@with-madrid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithIO/django-wools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
