# -*- coding: utf-8 -*-
from camcomskin.padova.interfaces import IRatingEnabled
from persistent.dict import PersistentDict
from plone import api
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import json


class ManageRating(BrowserView):

    def storage(self):
        annotations = IAnnotations(self.context)
        if 'collective.rating.values' not in annotations:
            annotations['collective.rating.values'] = PersistentDict({})
        return annotations['collective.rating.values']

    def update_rating(self):
        if api.user.is_anonymous():
            return
        current_rating = self.request.get('current_rating', None)
        if current_rating:
            annotations = self.storage()
            username = api.user.get_current().getUserName()
            annotations[username] = {
                'user': username,
                'rating_value': current_rating,
            }

    def delete_rating(self):
        if api.user.is_anonymous():
            return
        annotations = self.storage()
        username = api.user.get_current().getUserName()
        if username in annotations.keys():
            del annotations[username]
            return json.dumps({'ok': True})
        else:
            return json.dumps({'ok': False})

    def get_rating(self):
        annotations = self.storage()
        username = api.user.get_current().getUserName()
        if username in annotations.keys():
            return json.dumps(
                {'current_value': annotations[username]['rating_value']}
            )
        else:
            return json.dumps({'current_value': 0})

    def get_star_size(self):
        return json.dumps({
            'max_rating': 5,
        })

    def get_avg_rating(self):
        avg_rating = self.calculate_avg_rating()
        num_rating = self.num_rating()
        return json.dumps({
            'avg_rating': avg_rating,
            'num_rating': num_rating,
        })

    def num_rating(self):
        annotations = self.storage()
        return len(annotations.keys())

    def calculate_avg_rating(self):
        annotations = self.storage()
        if annotations:
            num_rating = self.num_rating()
            sum_rating = reduce(
                (lambda x, y: float(x) + float(y)),
                self.rating_list(annotations))
            return float(float(sum_rating) / num_rating)
        else:
            return 0

    def rating_list(self, annotations):
        return map(lambda x: x['rating_value'], annotations.values())


class BaseRatingView(BrowserView):
    def get_canonical(self):
        context = self.context.aq_inner
        pcs = context.restrictedTraverse('@@plone_context_state')
        return pcs.canonical_object()


class CheckRatingAction(BaseRatingView):

    def check_rating_action_add(self):
        obj = self.get_canonical()
        if not IATDocument.providedBy(obj):
            return False
        return not IRatingEnabled.providedBy(obj)

    def check_rating_action_remove(self):
        obj = self.get_canonical()
        if not IATDocument.providedBy(obj):
            return False
        return IRatingEnabled.providedBy(obj)


class ToggleEnableRating(BaseRatingView):

    def add_interface(self):
        obj = self.get_canonical()
        if not IATDocument.providedBy(obj):
            api.portal.show_message(
                message=u'Impossibile abilitare il rating.',
                type='error',
                request=self.request
            )
            return self.request.response.redirect(obj.absolute_url())
        if not IRatingEnabled.providedBy(obj):
            alsoProvides(obj, IRatingEnabled)
            obj.reindexObject(idxs=['object_provides'])
            api.portal.show_message(
                message='Rating abilitato sul contenuto.',
                type='info',
                request=self.request)
        else:
            api.portal.show_message(
                message=u'Rating già abilitato sul contenuto.',
                type='warning',
                request=self.request)
        self.request.response.redirect(obj.absolute_url())

    def remove_interface(self):
        obj = self.get_canonical()
        if IRatingEnabled.providedBy(obj):
            noLongerProvides(obj, IRatingEnabled)
            obj.subsite_class = ''
            obj.reindexObject(idxs=['object_provides'])
            api.portal.show_message(
                message=u'Rating disabilitato sul contenuto.',
                type='info',
                request=self.request)
        else:
            api.portal.show_message(
                message=u'Il rating era già stato disabilitato sul contenuto.',
                request=self.request,
                type='warning')

        self.request.response.redirect(obj.absolute_url())
