from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from lavender.utils import check_nickname
from lavender.models import Quenta

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=75, required=True)
    consent = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username']
        errors = check_nickname(username)
        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return username

    def clean_consent(self):
        pass

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(max_length=75, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if User.objects.exclude(username=self.instance.username).filter(email=email).exists():
                raise forms.ValidationError('Этот адрес почты уже используется')
        return email


class QuentaForm(forms.ModelForm):
    class Meta:
        model = Quenta
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        quenta: Quenta = super().save(commit=False)
        quenta.player = self.user
        if commit:
            quenta.save()
        return quenta
