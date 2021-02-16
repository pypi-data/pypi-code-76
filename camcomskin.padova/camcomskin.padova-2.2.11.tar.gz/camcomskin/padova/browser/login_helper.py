# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api
from plone.api.exc import InvalidParameterError


class View(BrowserView):

    def get_providers(self):
        try:
            authomatic_view = api.content.get_view(
                name='authomatic-handler', context=self.context, request=self.request)
        except InvalidParameterError:
            return None
        return authomatic_view.providers()
