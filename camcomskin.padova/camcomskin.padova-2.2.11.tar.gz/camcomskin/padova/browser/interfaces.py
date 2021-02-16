# -*- coding: utf-8 -*-
from plone.app.discussion.interfaces import IDiscussionLayer
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IThemeSpecific(IDefaultPloneLayer, IDiscussionLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IThemeBaseView(Interface):
    """ """

    def getColumnsClasses():
        """Returns all CSS classes based on columns presence.
        """
