# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ariadne_extended',
 'ariadne_extended.contrib.waffle_graph',
 'ariadne_extended.cursor_pagination',
 'ariadne_extended.filters',
 'ariadne_extended.graph_loader',
 'ariadne_extended.payload',
 'ariadne_extended.resolvers',
 'ariadne_extended.utils',
 'ariadne_extended.uuid']

package_data = \
{'': ['*']}

install_requires = \
['ariadne>=0.12.0,<0.13.0',
 'django>=2.2,<=3.2',
 'djangorestframework>=3.7,<4.0',
 'pyhumps>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'ariadne-extended',
    'version': '0.2.0',
    'description': 'Ariadne contrib library for working with Django and GraphQL',
    'long_description': "# Ariadne Extended\n\nAriadne comes with a few contrib modules to support integration with Django. This module acts as an additional Django contrib module to reduce some of the boilerplate when integrating with Django.\n\nIt copies and follows some of the conventions defined in Django Rest Framework, effort will be made to provide API compatibility with certain DRF extension modules that are relevant.\n\nThe overall goal is to provide often re-used modules and GrpahQL schema, so one doesn't have to re-create them per project.\n\n## Supported DRF modules\n\n* Pagination classes\n* Permissions classes\n* Serializer classes ( may not removed and made generic )\n* Throttling\n* django-filters filter backend\n\n## Supported Django versions\n\n**2.2.*, 3.0.\\***\n\n\n### `ariadne_extended.graph_loader`\n\nauto schema, resolver and types loader \n\nSearches for `types` and `resolvers` modules as well as any `.graphql` files defined within any installed Django application.\n\nOnce found they can be used to build the final schema and resolver solution for your ariadne application.\n\n### `ariadne_extended.payload`\nSchema, types and resolvers for the graphql `Payload` interface.\n\nCurrently the `FieldErrors` are highly coupled to Django rest framework field validation exceptions.\n\n### `ariadne_extended.cursor_pagination`\nRename to relay_pagination maybe?\n\nContains the `PageInfo` graphql type and `Connection` interface for utilizing cursor based pagination.\n\nTODO: Should we provide a input type for cursor pagination instead of just copying pagination args info paginate-able list fields??\n\n### `ariadne_extended.filters`\nFilter backend interface to pass filter arguments to django-filter.\n\n### `ariadne_extended.resolvers`\nABC for Class Based Resolvers and model resolvers that utilize DRF serializers for saving data. This is likely to change in the future.\n\n### `ariadne_extended.uuid`\nDRF UUID field scalar for use with models that may use a UUID as their primary key, or other UUID fields.\n\n## Contrib\n\n### `django-waffle` in `ariadne_extended.contrib.waffle_graph`\n\nAdds resolvers, schema and types that can be utilized to query the any waffle flags, samples and switches.\n\n\n# Checklist\n- [ ] Get rid of dependency on DRF?\n- [ ] Investigate the need for a serializer ( nested data reliance? )\n- [x] Organize code into multiple Django apps to select desired componentry\n- [ ] Documentation and examples\n- [ ] Better support of lists of enums when used with django-filters ( currently expects comma sep list string, not a list of enums from input field resolver )\n- [x] License and make public\n- [ ] Deployment automation\n- [ ] Mixins are highly coupled to serializers, should they still be?\n",
    'author': 'Patrick Forringer',
    'author_email': 'pforringer@patriotrc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/patriotresearch/ariadne-extended',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
