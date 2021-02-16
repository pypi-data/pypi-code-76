# -*- coding: utf-8 -*-
from collective.portletpage.browser.portletpage import TwoColumns
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PPHomepageView(TwoColumns):
    """Render a column
    """
    __call__ = ViewPageTemplateFile('templates/pp_homepage_view.pt')
