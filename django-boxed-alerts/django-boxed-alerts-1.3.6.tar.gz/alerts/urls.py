#
# Copyright 2013, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.
#
"""Alerts urls"""

from django.conf.urls import url, include
from .views import (
    UserSettingUpdate, UserSettingsList,
    MarkAllViewed, MarkAllDeleted, MarkViewed,
    MarkDeleted, AlertList, AlertsJson, Subscribe, Unsubscribe,
    MessageList, MessageThread, CreateMessage,
)

def url_tree(regex, *urls):
    """Provide a way to extend patterns easily"""
    class UrlTwig(object): # pylint: disable=too-few-public-methods, missing-docstring
        urlpatterns = urls
    return url(regex, include(UrlTwig))

urlpatterns = [ # pylint: disable=invalid-name
    url(r'^$', AlertList.as_view(), name="alerts"),
    url(r'^dm/$', MessageList.as_view(), name="messages"),
    url(r'^dm/(?P<pk>\d+)/$', MessageThread.as_view(), name="message.thread"),
    url(r'^message/$', CreateMessage.as_view(), name="message.new"),
    url(r'^message/(?P<pk>\d+)/$', CreateMessage.as_view(), name="message.reply"),
    url(r'^json/$', AlertsJson.as_view(), name="alerts.json"),
    url(r'^view/$', MarkAllViewed.as_view(), name="alert.view"),
    url(r'^delete/$', MarkAllDeleted.as_view(), name='alert.delete'),
    url(r'^settings/$', UserSettingsList.as_view(), name='alert.settings'),

    url_tree(
        r'^(?P<pk>\d+)/',
        url(r'^delete/', MarkDeleted.as_view(), name='alert.delete'),
        url(r'^view/', MarkViewed.as_view(), name="alert.view"),
    ),
    url_tree(
        r'^(?P<slug>[^\/]+)/',
        url(r'^$', AlertList.as_view(), name="alert.category"),
        url(r'^settings/$', UserSettingUpdate.as_view(), name='alert.settings'),
        url_tree(
            r'^subscribe/',
            url(r'^$', Subscribe.as_view(), name='alert.subscribe'),
            url(r'^(?P<pk>\d+)/$', Subscribe.as_view(), name='alert.subscribe'),
        ),
        url_tree(
            r'^unsubscribe/',
            url(r'^$', Unsubscribe.as_view(), name='alert.unsubscribe'),
            url(r'^(?P<pk>\d+)/$', Unsubscribe.as_view(), name='alert.unsubscribe'),
        ),
    ),
]
