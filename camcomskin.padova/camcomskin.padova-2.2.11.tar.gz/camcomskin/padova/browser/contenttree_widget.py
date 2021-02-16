# -*- coding: utf-8 -*-
from plone.formwidget.contenttree.widget import Fetch as BaseFetch
from zope.component import getMultiAdapter
from plone.formwidget.contenttree.utils import closest_content
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy

WHITELIST_WIDGETS = [
    'collective-tiles-collection-collection_uid',
]


class Fetch(BaseFetch):

    def __call__(self):
        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()

        widget = self.context
        context = widget.context

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        widget.update()
        source = widget.bound_source

        # Convert token from request to the path to the object
        token = self.request.form.get('href', None)
        directory = self.context.bound_source.tokenToPath(token)
        level = self.request.form.get('rel', 0)
        navtree_query = source.navigation_tree_query.copy()

        if widget.show_all_content_types and 'portal_type' in navtree_query:
            del navtree_query['portal_type']

        if directory is not None:
            navtree_query['path'] = {'depth': 1, 'query': directory}
        # This is the patch
        if 'is_default_page' not in navtree_query and widget.id not in WHITELIST_WIDGETS:  # noqa
            navtree_query['is_default_page'] = False
        # end patch

        content = closest_content(context)

        strategy = getMultiAdapter((content, widget), INavtreeStrategy)
        catalog = api.portal.get_tool(name='portal_catalog')

        children = []
        for brain in catalog(navtree_query):
            newNode = {'item': brain,
                       'depth': -1,  # not needed here
                       'currentItem': False,
                       'currentParent': False,
                       'children': []}
            if strategy.nodeFilter(newNode):
                newNode = strategy.decoratorFactory(newNode)
                children.append(newNode)

        self.request.response.setHeader('X-Theme-Disabled', 'True')

        return self.fragment_template(children=children, level=int(level))
