# Using example inspired on the github below: Thanks!
# https://github.com/nathanbigaignon/django-uikit-admin/blob/master/uikit_admin/templatetags/uikit_admin.py

from django import template
from django.forms.boundfield import BoundField
from django.utils.html import format_html

from django.forms.widgets import Select
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, AdminTextareaWidget

register = template.Library()


@register.simple_tag
def uka_form_row_stacked(element, errors='', extra_classes=''):
    label = BoundField.label_tag(element, "", {'class': 'uk-form-label'}, label_suffix='')
    
    if errors:
        extra_classes = f'{extra_classes} uk-form-danger uk-clearfix'
    
    help_text = f'<div class="uk-text-muted uk-margin-small-top"><span uk-icon="icon: comment"></span> {element.help_text}</div>' \
        if element.help_text else ''
    
    original_classes = element.field.widget.attrs.get('class', '')
    
    applied_classes = 'uk-margin-small-top uk-margin-small-bottom'
    
    if element.field.widget.__class__.__name__ == "Select":
        applied_classes = f'{original_classes} uk-select'
    
    elif element.field.widget.__class__.__name__ == "RelatedFieldWidgetWrapper":
        applied_classes = f'{original_classes} uk-select'
        
    elif element.field.widget.__class__.__name__ in ["AdminTextareaWidget", "TextareaWidget"]:
        applied_classes = f'{original_classes} uk-textarea'
    else:
        applied_classes = original_classes
    
    
    # Trying some overrides
    if element.field.__class__.__name__ in ['SplitDateTimeField', 'ReadOnlyPasswordHashField', 'ModelMultipleChoiceField']:
        element = element.as_widget()
    
    elif element.field.__class__.__name__ == 'TextareaWidget':
        element = element.as_widget(attrs={'class': f'{applied_classes}'})
   
    else:
        element = element.as_widget(attrs={'class': f'uk-input uk-form-width-large {applied_classes} {extra_classes}'})
    
    html_error = format_html(f'<div class="uk-text-danger uk-margin-top">{errors}</div>')
    
    html = format_html(f'<div class="uk-form-row">' \
                       f'    <div>{label} {html_error}</div>' \
                       f'    <div class="uk-form-controls" style="clear: both">{element}{help_text}</div>' \
                       f'</div>')
    return html

@register.simple_tag
def uk_element (element, css_class_override=None):
    
    if css_class_override is not None:
        element = element.as_widget(attrs={'class': css_class_override })
    else:
        element = element.as_widget()
        
    return format_html(element)
    

@register.simple_tag
def uka_form_row_stacked_button(text, classes=None):  # @todo Fix this
    if classes is None:
        classes = ''
    html = format_html(f'<div class="uk-form-row"><div class="uk-form-controls"><button class="uk-button {classes}">{text}</button></div></div>')
    return html


@register.simple_tag
def uka_button(text, classes=None, type_name=None, name=None):
    if classes is None:
        classes = ''
    if type_name is None:
        type_name = ''
    if name is None:
        name = ''
    html = format_html(
        '<button class="uk-button {}" type="{}" name="{}">{}</button>',
        classes, type, name, text)
    return html


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})