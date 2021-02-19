from django.urls import re_path

from molo.commenting import views
from molo.commenting.views import CommentReplyView

urlpatterns = [
    re_path(r'molo/report/(\d+)/$', views.report, name='molo-comments-report'),
    re_path(
        r'^comments/reported/(?P<comment_pk>\d+)/$',
        views.report_response, name='report_response'),

    re_path(
        r'molo/reply/(?P<parent_comment_pk>\d+)/$',
        CommentReplyView.as_view(),
        name='molo-comments-reply'),

    re_path(
        r'molo/post/$',
        views.post_molo_comment, name='molo-comments-post'),

    re_path(
        r'molo/(?P<page_id>\d+)/comments/$',
        views.view_more_article_comments,
        name='more-comments'),

    re_path(
        r'molo/replies/$',
        views.reply_list, name='reply_list'),
]
