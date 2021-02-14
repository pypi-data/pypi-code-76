from django import forms
#from base.widgets import ClearableUUIDSecureFileInput
#from django_select2.forms import Select2Widget

class PrlModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(PrlModelForm, self).__init__(*args, **kwargs)

        # Overriding File Field
        print(self.fields)

        for key in self.fields.keys():
            field_type = type(self.fields[key]).__name__

            #print(f'FIELD TYPE: {field_type}')

            #if field_type == 'CharField':
            widget_type = type(self.fields[key].widget).__name__

            if widget_type == 'AdminTextareaWidget':
                self.fields[key].widget.attrs['class'] = \
                    self.fields[key].widget.attrs['class'] + ' uk-textarea'
            elif widget_type == 'AdminTextInputWidget':
                self.fields[key].widget.attrs['class'] = \
                    self.fields[key].widget.attrs['class'] + ' uk-input'

            #self.fields[key].widget.attrs['class'] = self.fields[key].widget.attrs['class'] + ' uk-input'

            #if field_type == 'FileField':
            #    self.fields[key].widget = ClearableUUIDSecureFileInput()
