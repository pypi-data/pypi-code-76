from django import forms
from django.forms import ModelForm
from .models import BuybackSettings
from django_eveonline_connector.models import EveEntity


class EveBuyback(forms.Form):
    submission = forms.CharField(widget=forms.Textarea)


class EveBuybackSettingsForm(ModelForm):
    contract_entity = forms.ModelChoiceField(
        queryset=EveEntity.objects.all().order_by('name'), required=False)

    class Meta:
        model = BuybackSettings
        fields = '__all__'
