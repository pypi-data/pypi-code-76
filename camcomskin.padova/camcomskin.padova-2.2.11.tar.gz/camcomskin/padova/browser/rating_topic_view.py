# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.discussion.interfaces import IConversation
from Products.Five import BrowserView

import json


class View(BrowserView):
    def get_average_rating(self, item):
        try:
            avg_view = api.content.get_view(
                name='get_avg_rating', context=item, request=self.request
            )
            star_size_view = api.content.get_view(
                name='get_star_size', context=item, request=self.request
            )
        except InvalidParameterError:
            return ''
        avg_data = json.loads(avg_view())
        star_size = json.loads(star_size_view())
        return json.dumps(
            {
                'rating': avg_data.get('avg_rating'),
                'max_rating': star_size.get('max_rating'),
            }
        )

    def get_comments(self, item):
        try:
            return IConversation(item)
        except Exception:
            return None

    def get_comments_count(self, item):
        comments = self.get_comments(item)
        if not comments:
            return 0
        return comments.total_comments

    def get_last_comments(self, item):
        """ """
        try:
            comments_to_show = api.portal.get_registry_record(
                'partecipazione.attiva.comments_to_show'
            )
        except InvalidParameterError:
            return []
        if not comments_to_show:
            return []
        comments = self.get_comments(item)
        if not comments:
            return []
        return [x for x in comments.values()][-comments_to_show:]

    def format_time(self, time):
        # We have to transform Python datetime into Zope DateTime
        # before we can call toLocalizedTime.
        util = api.portal.get_tool(name='translation_service')
        zope_time = DateTime(time.isoformat())
        return util.toLocalizedTime(zope_time, long_format=True)
