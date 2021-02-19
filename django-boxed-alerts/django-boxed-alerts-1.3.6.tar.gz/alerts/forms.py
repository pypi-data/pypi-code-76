#
# Copyright 2016, Martin Owens <doctormo@gmail.com>
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
"""
Forms for the alert system
"""

import json
import logging

from django.forms import (
    BaseFormSet, BaseModelFormSet, modelformset_factory,
    ModelForm, IntegerField, BooleanField,
    HiddenInput
)
from django.urls import reverse
from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Message, AlertType, AlertSubscription, UserAlertSetting

class MessageForm(ModelForm):
    reply_to = IntegerField(widget=HiddenInput, required=False)
    recipient = IntegerField(widget=HiddenInput)

    class Meta:
        model = Message
        fields = ('subject','body', 'recipient', 'reply_to')

    def clean_recipient(self):
        pk = self.cleaned_data['recipient']
        return get_user_model().objects.get(pk=pk)

    def clean_reply_to(self):
        pk = self.cleaned_data['reply_to']
        if pk:
            return Message.objects.get(pk=pk)


class SettingsBaseFormSet(BaseModelFormSet):
    def __init__(self, instance, *args, **kw):
        self.user = instance
        self._qset = None
        super(SettingsBaseFormSet, self).__init__(*args, **kw)

    def get_queryset(self):
        """Return a fixed list of alert_settings (not a queryset)"""
        # WARNING: django will eat any and all AttributeErrors from this code,
        # be careful when developing as you may find settings just disapear
        # after the first one or when the error would hit.
        if self._qset is None:
            try:
                self._qset = list(self._generate_settings())
            except AttributeError as err:
                raise IOError(err)
        return self._qset

    def _generate_settings(self):
        """Generate a list of UserAlertSetting, some exist, some do not"""
        done = []

        user_subs = AlertSubscription.objects.filter(user_id=self.user.pk)
        subscrips = Prefetch('alert__subscriptions', to_attr='user_subs', queryset=user_subs)
        user_sets = UserAlertSetting.objects.filter(user_id=self.user.pk)
        #settings = Prefetch('settings', to_attr='user_settings', queryset=user_sets)

        # For all the existing settings (saved in the database)
        for setting in user_sets.select_related('alert').prefetch_related(subscrips):
            try:
                if setting.alert.subscribe_own is not None:
                    done.append(setting.alert.slug)
                    yield setting
            except (KeyError, AttributeError):
                # Don't add stale/old settings, delete them
                logging.warning("Deleting setting %s", str(setting))
                setting.delete()

        subscrips = Prefetch('subscriptions', to_attr='user_subs', queryset=user_subs)

        # Now get all the default settings for things we should be able to see
        for alert in AlertType.objects.exclude(slug__in=done).prefetch_related(subscrips):
            if alert.show_settings:
                yield UserAlertSetting(user=self.user, alert=alert)

    def _construct_form(self, i, **kwargs):
        """
        We have a mixture of real instances and non-real instances so we
        need to control the construction carefully for the POST operation.
        """
        if self.is_bound and i < self.initial_form_count():
            alert_id = self.data["%s-%s" % (self.add_prefix(i), 'alert')]
            for obj in self.get_queryset():
                if str(obj.alert_id) == str(alert_id):
                    kwargs['instance'] = obj
            # Note use of parent's parent construct_form call here.
            return BaseFormSet._construct_form(self, i, **kwargs) #pylint: disable=protected-access
        return super(SettingsBaseFormSet, self)._construct_form(i, **kwargs)

    @property
    def media(self):
        """We want all the forms media added together"""
        media = super(SettingsBaseFormSet, self).media
        for form in self.forms[1:]:
            media += form.media
        return media



class SettingsForm(ModelForm):
    suball = BooleanField(required=False, label=_("Subscribe to All"),
        help_text=_("<strong>Warning!</strong> This can result in a lot of messages."))
    em_msg = _("<strong>Warning!</strong> You haven't told us your mail addres"
               "s yet! If you would like to receive emails from inkscape.org, "
               "enter an email address <a href='%(url)s'>in your profile</a>.")

    class Meta:
        model = UserAlertSetting
        fields = ('alert', 'email', 'irc', 'batch', 'owner', 'suball', 'custom_settings')

    def __init__(self, *args, **kw):
        super(SettingsForm, self).__init__(*args, **kw)
        self.fields['alert'].widget = HiddenInput()
        self.fields['custom_settings'].widget = HiddenInput()
        self.setup()

    def setup(self):
        """Set up the form based on various settings and availability"""
        try:
            self.subs = self.instance.alert.user_subs
        except AttributeError:
            all_subs = self.instance.alert.subscriptions
            self.subs = list(all_subs.filter(user_id=self.instance.user_id))
        # XXX Replace with "disabled" class and change help_text
        if not self.instance.user.ircnick:
            self.fields.pop('irc')
        if not self.instance.user.email:
            self.fields['email'].widget.attrs['disabled'] = 'disabled'
            self.fields['email'].help_text = self.em_msg % {'url': reverse('edit_profile')}
        if not self.instance.alert.subscribe_own:
            self.fields.pop('owner')
            # XXX the name of this field needs to change depending on if subscribe is visible at all.
        if self.instance.alert.subscribe_all:
            suball = [sub is None for sub in self.subs if sub.target is None]
            self.fields['suball'].initial = len(suball) == 1
        else:
            self.fields.pop('suball')

        # Apply the custom field widget/field as needed
        self.custom = []
        data = self.instance.get_custom_settings()
        for name, field in self.instance.alert.get_custom_fields(data, user=self.instance.user):
            self.custom.append(name)
            self.fields[name] = field
            if name in data:
                self.initial[name] = data[name]

        if self.instance.alert.subscribe_any:
            for sub in self.subs:
                if sub.target is None:
                    continue
                try:
                    label = _("Subscription to %s") % str(sub.object())
                    field = BooleanField(required=False, label=label)
                    field.delete = True
                    self.fields['delete_%d' % sub.pk] = field
                except sub.model.DoesNotExist:
                    sub.delete()

    def clean(self):
        """Turn custom setting fields into json data"""
        super().clean()
        # We actually ignore any data that was sent to us in the custom_settings field
        self.cleaned_data['custom_settings'] = json.dumps(dict([
            (field, self.cleaned_data[field])\
                for field in self.custom if field in self.cleaned_data]))
        return self.cleaned_data

    def save(self, commit=True):
        """Save the form, making sure to update subscriptions and custom settings"""
        ret = super().save(commit=commit)
        if commit:
            alert = self.instance.alert

            # Update subscriptions
            subs = alert.subscriptions.filter(user_id=self.instance.user_id)
            if self.instance.alert.subscribe_all:
                if self.cleaned_data.get('suball', False):
                    AlertSubscription.objects.get_or_create(None,\
                        alert_id=self.instance.alert_id,\
                        user_id=self.instance.user_id)
                else:
                    subs.filter(target__isnull=True).delete()
            if not alert.subscribe_any:
                subs.filter(target__isnull=False).delete()
            for name, to_delete in self.cleaned_data.items():
                if name.startswith('delete_') and to_delete:
                    subs.filter(pk=int(name.split('_')[-1])).delete()
        return ret

    @property
    def label(self):
        if not self.instance.pk:
            return str(self.instance) + "*"
        return str(self.instance)

    @property
    def description(self):
        return self.instance.alert.info


SettingsFormSet = modelformset_factory(
    model=UserAlertSetting,
    form=SettingsForm,
    formset=SettingsBaseFormSet, extra=0)
