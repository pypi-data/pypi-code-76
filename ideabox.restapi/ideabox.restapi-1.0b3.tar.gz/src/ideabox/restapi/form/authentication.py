# -*- coding: utf-8 -*-

from imio.restapi.interfaces import IRestAuthentication
from plone import api
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


@implementer(IRestAuthentication)
@adapter(IBrowserRequest)
class IdeaboxAuthentication(object):

    def __init__(self, request):
        self.request = request

    @property
    def basic(self):
        return (
            api.portal.get_registry_record("ideabox.restapi.login"),
            api.portal.get_registry_record("ideabox.restapi.password"),
        )
