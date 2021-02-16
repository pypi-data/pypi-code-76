# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.contentleadimage.browser.viewlets import (
    LeadImageViewlet as BaseLeadImageViewlet,
)  # noqa
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from plone import api
from plone.app.discussion.browser.comments import CommentsViewlet
from plone.app.layout.viewlets import common as base
from plone.app.layout.viewlets.content import (
    ContentRelatedItems as BaseContentRelatedItems,
)  # noqa
from plone.app.layout.viewlets.content import (
    DocumentBylineViewlet as BaseDocumentBylineViewlet,
)  # noqa
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from urllib2 import quote
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.app.discussion.interfaces import IDiscussionSettings


SHARES = {
    'facebook': {
        'share_url': 'https://www.facebook.com/sharer/sharer.php?u={0}',
        'label': 'Facebook',
        'cssClass': 'fab fa-facebook-f',
    },
    'twitter': {
        'share_url': 'https://twitter.com/intent/tweet?url={0}&text={1}',
        'label': 'Twitter',
        'cssClass': 'fab fa-twitter',
    },
    'google': {
        'share_url': 'https://plus.google.com/share?url={0}',
        'label': 'Google',
        'cssClass': 'fab fa-google-plus-g',
    },
    'linkedin': {
        'share_url': 'http://www.linkedin.com/shareArticle?url={0}&title={1}',
        'label': 'Linkedin',
        'cssClass': 'fab fa-linkedin-in',
    },
    'pinterest': {
        'share_url': 'https://pinterest.com/pin/create/bookmarklet/?media={0}&url={1}&is_video={2}&description={3}',  # noqa
        'label': 'Pinterest',
        'cssClass': 'fab fa-pinterest',
    },
    'pocket': {
        'share_url': 'https://getpocket.com/save?url={0}&title={1}',
        'label': 'Pocket',
        'cssClass': 'fab fa-pocket',
    },
    'telegram': {
        'share_url': 'https://telegram.me/share/url?url={0}&text={1}',
        'label': 'Telegram',
        'cssClass': 'fab fa-telegram',
    },
}


class LeadImageViewlet(BaseLeadImageViewlet):
    def descTag(self, css_class='tileImage'):
        """ returns img tag """
        context = aq_inner(self.context)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None and field.get_size(context) != 0:
            scale = self.prefs.desc_scale_name
            return field.tag(
                context,
                scale=scale,
                css_class=css_class,
                title="immagine",
                alt="immagine",
            )
        return ''


class DocumentBylineViewlet(BaseDocumentBylineViewlet):

    index = ViewPageTemplateFile("templates/document_byline.pt")

    def show(self):
        return True


class ContentRelatedItems(BaseContentRelatedItems):
    def related2brains(self, related):
        """Return a list of brains based on a list of relations. Will filter
        relations if the user has no permission to access the content.

        :param related: related items
        :type related: list of relations
        :return: list of catalog brains.

        Customization: if the related item doesn't exists anymore, path is None
        so don't try to make a catalog search (that raise and exception)
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = []
        for r in related:
            path = r.to_path
            if path:
                # the query will return an empty list if the user has no
                # permission to see the target object
                brains.extend(catalog(path=dict(query=path, depth=0)))
        return brains


class SocialViewlet(base.ViewletBase):
    def __init__(self, context, request, view, manager):
        super(SocialViewlet, self).__init__(context, request, view, manager)

    def get_css_class(self, social_type):
        cssClass = SHARES[social_type]['cssClass']
        return cssClass or ''

    def get_sharer_url(self, social_type):
        share_url = SHARES[social_type]['share_url']
        #  title = quote(self.context.title)
        title = quote(self.context.Title())
        item_url = self.context.absolute_url()
        if social_type == 'linkedin':
            return share_url.format(item_url, self.context.title)
        if social_type == 'twitter':
            return share_url.format(item_url, title)
        if social_type == 'pinterest':
            return share_url.format('', item_url, 'false', title)
        if social_type == 'pocket':
            return share_url.format(item_url, title)
        if social_type == 'telegram':
            return share_url.format(item_url, title)
        return share_url.format(item_url)

    def get_socials(self):
        return ('facebook', 'twitter', 'google', 'telegram')


class PersonalBarViewlet(base.PersonalBarViewlet):
    """
    Override of Personal Bar
    Conditional rendering of this for user roles
    If the user has only `authenitcated` can't see the personal bar
    """

    def userHasEnoughPermissions(self):
        """
        Checks user permissions
        Returns True if the user has not only the role `authenticated`
        """
        if self.anonymous:
            return False

        user_roles = self.portal_state.member().getRoles()
        return len(user_roles) > 1

    def render(self):
        """
        Render viewlet only if the user has enough permissions
        """

        if self.userHasEnoughPermissions():
            # Call parent method
            return super(PersonalBarViewlet, self).render()
        else:
            # No output, the viewlet is disabled
            return ""


class CCPDCommentsViewlet(CommentsViewlet):
    index = ViewPageTemplateFile('templates/comments_viewlet.pt')

    @property
    def isAdmin(self):
        return api.user.has_permission('Manage portal')

    def show_commenter_image(self):
        # Check if showing commenter image is enabled in the registry
        if not self.isAdmin:
            return False
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        return settings.show_commenter_image
