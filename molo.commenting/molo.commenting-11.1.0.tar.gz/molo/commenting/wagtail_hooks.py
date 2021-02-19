from django.conf.urls import re_path
from molo.commenting.admin import CommentingModelAdminGroup
from molo.commenting.admin_views import MoloCommentsAdminReplyView
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import modeladmin_register


@hooks.register('register_admin_urls')
def register_molo_comments_admin_reply_url():
    return [
        re_path(
            r'comment/(?P<parent>\d+)/reply/$',
            MoloCommentsAdminReplyView.as_view(),
            name='molo-comments-admin-reply'),
    ]


modeladmin_register(CommentingModelAdminGroup)
