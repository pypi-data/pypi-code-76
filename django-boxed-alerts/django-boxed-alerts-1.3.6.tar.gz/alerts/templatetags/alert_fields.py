#
# Copyright 2017, Martin Owens <doctormo@gmail.com>
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
Provide a template tag that allows for translated fields to be looked up.

Assumptions:
  * Target model has related_name 'translations'.
  * Target model and language have unique together set.
  * Target field and translated field have the same name.

{% load i18n_fields %}

{{ object|translate_field:"field_name" }}
"""
from datetime import timedelta, datetime

from django.utils import timezone
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.template import Library, TemplateSyntaxError
from django.template.defaultfilters import date, timesince
from django.templatetags.tz import localtime
from django.forms import widgets
from django.conf import settings
from django.urls import resolve

from django.core.cache import caches
CACHE = caches['default']

register = Library() # pylint: disable=invalid-name

DEFAULT_LANG = settings.LANGUAGE_CODE.split('-')[0]
OTHER_LANGS = list(i for i in settings.LANGUAGES if i[0].split('-')[0] != DEFAULT_LANG)

CONF_ERR = "Model '{}' is not configured for translations."
FIELD_ERR = "Field '{}.{}' doesn't exist, so it can't be translated."
STR_ERR = "Expected object but got string '{}'"

@register.filter("translate_field")
def translate_field(obj, name):
    """Attempt to translate the names field if the object supports a simple i18n translations"""
    if obj in ('', None, 0):
        return obj

    if isinstance(obj, str):
        raise TemplateSyntaxError(STR_ERR.format(obj))

    # Check that this is a translated model
    try:
        Translations = obj.translations.model # pylint: disable=invalid-name
    except AttributeError:
        raise TemplateSyntaxError(CONF_ERR.format(type(obj).__name__))

    # Check both target and translation model have the requested field
    for cls in (type(obj), Translations):
        try:
            cls._meta.get_field(name)
        except FieldDoesNotExist:
            raise TemplateSyntaxError(FIELD_ERR.format(cls.__name__, name))

    lang = get_language()
    if lang or lang != DEFAULT_LANG:
        key = '{}.{}.{}'.format(type(obj).__name__, obj.pk, lang)
        tr_obj = CACHE.get(key)
        if tr_obj is None:
            try:
                # Return the translation OR if the translation exists, but the
                # field is blank, return the English version instead.
                tr_obj = obj.translations.get(language=lang)
            except Translations.DoesNotExist:
                tr_obj = False
            CACHE.set(key, tr_obj)
        if tr_obj is False:
            tr_obj = obj

        if hasattr(tr_obj, name):
            return getattr(tr_obj, name)

    # Passthrough, nothing to do here.
    return getattr(obj, name)

@register.filter("placeholder")
def add_placeholder(bound_field, text=None):
    """Add a placeholder attribute to any form field object"""
    if text is None:
        raise ValueError("Placeholder requires text content for widget.")
    if type(bound_field.field).__name__ == 'ReCaptchaField':
        return bound_field
    bound_field.field.widget.attrs.update({"placeholder": text})
    return bound_field

@register.filter("autofocus")
def add_autofocus(bound_field):
    """Add an autofocus attribute to any form field object"""
    bound_field.field.widget.attrs.update({"autofocus": "autofocus"})
    return bound_field

@register.filter("tabindex")
def add_tabindex(bound_field, number):
    """Add table attribute to any form field object"""
    bound_field.field.widget.attrs.update({"tabindex": number})
    return bound_field

@register.filter("formfield")
def add_form_control(bound_field):
    """Add a form-control attribute to any form field"""
    if isinstance(bound_field.field.widget, widgets.CheckboxSelectMultiple):
        return bound_field

    cls = ['form-control']
    if bound_field.errors:
        cls.append("form-control-danger")
    bound_field.field.widget.attrs.update({"class": ' '.join(cls)})
    return bound_field

@register.filter("is_checkbox")
def is_checkbox_field(bound_field):
    """Returns true if the form field object is a checkbox"""
    return type(bound_field.field.widget).__name__ == 'CheckboxInput'


@register.filter("title")
def title(orig, view):
    """Attempt to get the title from the view"""
    if orig in [None, '']:
        if hasattr(view, 'title'):
            return view.title
        elif hasattr(view, 'get_title'):
            return view.get_title()
        return None
    return orig

@register.simple_tag(name="now")
def _dt(arg=None):
    if not arg:
        return datetime.now(timezone.utc)
    elif isinstance(arg, str):
        try:
            (dat, time) = arg.split(' ')
            dat = [int(i) for i in dat.split('-')[:3] + time.split(':')[:3]]
            return datetime(*(dat + [0, timezone.utc]))
        except Exception:
            raise ValueError("Should be a datetime object, got string: %s" % arg)
    elif not isinstance(arg, datetime) or not arg.tzinfo:
        return datetime(arg.year, arg.month, arg.day,
                        arg.hour, arg.minute, arg.second,
                        arg.microsecond, timezone.utc)
    return arg

@register.filter("timetag", is_safe=True)
def timetag_filter(value, arg=None):
    """Formats a date as a time since if less than 1 day old or as a date otherwise
    Will return <time...> html tag as part of the output.
    """
    if not value:
        return ''
    value = _dt(value)
    arg = _dt(arg)

    if arg - value > timedelta(days=1):
        label = date(value, 'Y-m-d')
    else:
        label = timesince(value, arg) + " ago"

    return mark_safe("<time datetime=\"%s\" title=\"%s\">%s</time>" % (
        date(value, 'Y-m-d\\TH:i:sO'), date(localtime(value), 'Y-m-d H:i:sO'), label))

@register.filter("querydict_pop")
def kwarg_remove(qdict, item):
    """Removes a QueryDict item"""
    qdict = qdict.copy()
    qdict.pop(item, None)
    return qdict

@register.simple_tag(takes_context=True)
def url_name(context, equal=None, okay="active", nok=""):
    """Return the url_name for this page"""
    name = resolve(context['request'].path_info).url_name
    if equal:
        return okay if name == equal else nok
    return name
