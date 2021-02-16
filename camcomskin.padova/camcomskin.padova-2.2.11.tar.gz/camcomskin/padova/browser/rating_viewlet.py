# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from plone import api
from urllib import quote


class RatingManagerViewlet(ViewletBase):

    # def rating_is_active(self):
    #     field = self.context.getField('active_rating')
    #     if not field:
    #         return False
    #     return field.get(self.context)

    def can_rate(self):
        return not api.user.is_anonymous()

    def render(self):
        return self.index()

    def generate_came_from(self):
        return '{0}/login?came_from={1}'.format(
            self.context.portal_url(),
            quote(self.context.absolute_url())
        )
