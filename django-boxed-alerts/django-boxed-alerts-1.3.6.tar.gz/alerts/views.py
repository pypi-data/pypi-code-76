# -*- coding: utf-8 -*-
#
# Copyright 2014, Martin Owens <doctormo@gmail.com>
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
import json

from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.db.models import Func, Q
from django.conf import settings

from .forms import MessageForm, SettingsForm
from .mixins import NeverCacheMixin, UserRequiredMixin, UserMixin, OwnerRequiredMixin
from .models import UserAlert, Message, UserAlertSetting, AlertType, AlertSubscription

class AlertsJson(NeverCacheMixin, UserRequiredMixin, View):
    def get(self, request):
        alerts = request.user.alerts.all()
        context = {
            'types': tuple(AlertType.objects.values()) or None,
            'new': tuple(alerts.new.values()) or None,
        }
        return JsonResponse(context)

class IsNull(Func):
    template = "%(expressions)s IS NULL"

class AlertList(NeverCacheMixin, OwnerRequiredMixin, ListView):
    """Shows a list of user alerts, user only sees their own"""
    paginate_by = 15

    def get_queryset(self, **kwargs):
        qset = self.request.user.alerts.all().visible
        self.breadcrumb_root = self.request.user
        if 'slug' in self.kwargs:
            self.parent = get_object_or_404(AlertType, slug=self.kwargs['slug'])
            qset = qset.filter(alert__slug=self.kwargs['slug'])
        else:
            self.parent = (reverse('alerts'), _('Inbox'))

        if 'new' in self.request.GET:
            self.title = _("New")
            qset = qset.filter(viewed__isnull=True, deleted__isnull=True)
        qset = qset.annotate(not_viewed=IsNull('viewed'))
        qset = qset.prefetch_related('objs', 'objs__target', 'values')
        qset = qset.select_related('alert')
        return qset.order_by('-not_viewed', 'viewed', '-created')

    def get_context_data(self, **data):
        data = super(AlertList, self).get_context_data(**data)
        # Disable alert vew
        data['alerts'] = True
        return data




class MarkViewed(NeverCacheMixin, OwnerRequiredMixin, View, SingleObjectMixin):
    model = UserAlert
    function = 'view'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        getattr(obj, self.function)()
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponse(json.dumps({self.function: [obj.pk]}))


class MarkAllViewed(AlertList):
    function = 'view'

    def get(self, request, *args, **kwargs):
        objs = self.get_queryset()
        # This list() MUST happen before the function otherwise delete
        # will return an empty list and fail to update the html.
        pks = list(objs.values_list('pk', flat=True))

        getattr(objs, self.function + '_all')()
        return HttpResponse(json.dumps({self.function: list(pks)}))
 

class MarkDeleted(MarkViewed):
    function = 'delete'

class MarkAllDeleted(MarkAllViewed):
    function = 'delete'


class Subscribe(NeverCacheMixin, UserRequiredMixin, CreateView):
    model = AlertSubscription
    fields = [] # Everything is in url or context

    def get(self, request, **kwargs):
        if request.GET.get('post', False):
            return self.post(request, **kwargs)
        return super(Subscribe, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(Subscribe, self).get_context_data(**kwargs)
        self.breadcrumb_root = self.request.user
        data['alert'] = get_object_or_404(AlertType, slug=self.kwargs['slug'])
        data['object'] = data['alert']
        if 'pk' in self.kwargs:
            try:
                subscription = data['alert'].get_object(pk=self.kwargs['pk'])
            except data['alert'].sender.DoesNotExist:
                raise Http404("Alert subscription doesn't exist")

            data['object_name'] = data['alert'].get_object_name(subscription)
            data['title'] = _('Subscribe to %(object_name)s') % data
        else:
            data['alert_name'] = data['alert'].name
            data['title'] = _('Subscribe to All %(alert_name)s') % data
        return data

    def post(self, request, **kwargs):
        self.object = None
        data = self.get_context_data(**kwargs)
        kwargs = dict(user=request.user, target=self.kwargs.get('pk', None))
        (self.object, created, previous) = data['alert'].subscriptions.get_or_create(**kwargs)
        if previous:
            messages.warning(request,
                             _("Deleted %d previous subscription(s) (superseded)") % previous)
        if created:
            messages.info(request, _('Subscription created!'))
        else:
            messages.warning(request, _('Already subscribed to this!'))

        next_url = request.GET.get('next', request.POST.get('next', None))
        if not next_url:
            next_url = reverse('alert.settings') + '?tab=' + data['alert'].slug

        return HttpResponseRedirect(next_url)


class Unsubscribe(NeverCacheMixin, OwnerRequiredMixin, DeleteView):
    model = AlertSubscription

    def get(self, request, **kwargs):
        if request.GET.get('post', False):
            return self.post(request, **kwargs)
        return super(Unsubscribe, self).get(request, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next', self.request.POST.get('next', None))
        if not next_url:
            next_url = reverse('alert.settings')
        return next_url

    def get_context_data(self, **kwargs):
        data = super(Unsubscribe, self).get_context_data(**kwargs)
        self.breadcrumb_root = self.request.user
        data['alert'] = AlertType.objects.get(slug=self.kwargs['slug'])
        data['object'] = data['alert']
        data['delete'] = True
        if 'pk' in self.kwargs:
            subscription = data['alert'].get_object(pk=self.kwargs['pk'])
            data['object_name'] = data['alert'].get_object_name(subscription)
            data['title'] = _('Unsubscribe from %(object_name)s') % data
        else:
            data['alert_name'] = data['alert'].name
            data['title'] = _('Unsubscribe from All')
        return data
    
    def get_object(self):
        if 'slug' in self.kwargs:
            alert = get_object_or_404(AlertType, slug=self.kwargs['slug'])
            kw = dict(user=self.request.user)
            if 'pk' in self.kwargs:
                kw['target'] = self.kwargs['pk']
            else:
                kw['target__isnull'] = True
            return get_object_or_404(alert.subscriptions, **kw)
        return super(Unsubscribe, self).get_object()

class UserSettingUpdate(NeverCacheMixin, UserMixin, UpdateView):
    model = UserAlertSetting
    form_class = SettingsForm

    @property
    def title(self):
        return str(self.get_object())

    def get_object(self):
        try:
            return self.model.objects.get(user=self.request.user,
                                          alert__slug=self.kwargs['slug'])
        except self.model.DoesNotExist:
            alert = AlertType.objects.get(slug=self.kwargs['slug'])
            return alert.settings.for_user(self.request.user)

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        elif 'next' in self.request.POST:
            return self.request.POST['next']
        return reverse('alert.settings', kwargs=self.kwargs)

class UserSettingsList(NeverCacheMixin, UserMixin, ListView):
    title = _('All Notification Settings')
    template_name = 'alerts/useralertsetting_list.html'

    def get_queryset(self):
        done = []
        user = self.request.user
        user_sets = UserAlertSetting.objects.filter(user_id=user.pk)
        for setting in user_sets.select_related('alert'):
            alert = setting.alert
            alert.setting = setting
            yield alert
            done.append(alert.pk)

        for alert in AlertType.objects.exclude(slug__in=done):
            if alert.show_settings:
                yield alert

class MessageList(NeverCacheMixin, UserRequiredMixin, ListView):
    """List messages the user has been involved with"""
    model = Message
    paginate_by = 15

    def get_queryset(self):
        """Returns a list of root messages that user is involved in"""
        user = self.request.user
        return super().get_queryset()\
            .filter(Q(sender_id=user.pk) | Q(recipient_id=user.pk))\
            .filter(Q(reply_to__isnull=True) | Q(root__isnull=True))\
            .prefetch_related('thread').order_by('-created')

class MessageThread(NeverCacheMixin, UserRequiredMixin, ListView):
    """A single message thread from root to branch."""
    template_name = 'alerts/thread_list.html'
    model = Message
    paginate_by = 15

    def get_queryset(self):
        """Return the thread, generate it if it's blank"""
        user = self.request.user
        root = get_object_or_404(Message, pk=self.kwargs['pk'])
        if root.sender_id != user.pk and root.recipient_id != user.pk:
            raise Http404("No thread available for you.")
        thread = root.thread.all()
        if thread.count() == 0:
            root.remember_thread()
        return root.thread.all().order_by('-created')

class CreateMessage(NeverCacheMixin, UserRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        perm = getattr(settings, 'ALERTS_MESSAGE_PERMISSION', None)
        if perm and not self.request.user.has_perm(perm):
            perm_message = getattr(settings, 'ALERTS_MESSAGE_DENIED', _('Permission Denied'))
            messages.info(self.request, perm_message)
            return HttpResponseRedirect(self.request.user.get_absolute_url())

        obj = form.save(commit=False)
        obj.sender = self.request.user
        obj.save()
        messages.info(self.request, _('Message Sent to %s') % str(obj.recipient))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_profile')

    def get_reply_to(self):
        if 'pk' in self.kwargs:
            # If we ever want to restrict who can reply, do it here first.
            return get_object_or_404(self.model, pk=self.kwargs['pk'], recipient=self.request.user)

    def get_initial(self):
        """Add reply to subject initial data"""
        initial = super(CreateMessage, self).get_initial()
        self.recipient = get_object_or_404(get_user_model(), username=self.kwargs.get('username',''))
        rto = self.get_reply_to()
        if rto:
            initial['subject'] = rto.subject
            if not rto.reply_to:
                initial['subject'] = "Re: " + initial['subject']
        if 'pk' in self.kwargs:
            initial['reply_to'] = self.kwargs['pk']
        initial['recipient'] = self.recipient.pk
        return initial

    def get_context_data(self, **data):
        """Add reply to message object to template output"""
        data = super(CreateMessage, self).get_context_data(**data)
        data['reply_to'] = self.get_reply_to()
        data['recipient'] = self.recipient
        data['object_list'] = Message.objects.all()
        data['object_list'].parent = self.recipient

        data['title'] = _("Send New Message")
        if data['reply_to']:
            data['title'] = _("Send Reply Message")

        return data

