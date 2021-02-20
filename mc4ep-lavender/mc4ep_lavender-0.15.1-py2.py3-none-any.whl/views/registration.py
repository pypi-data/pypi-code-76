from uuid import uuid4

from lavender.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from lavender.models import Package, Token


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/profile')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=username, password=raw_password)
            user.packages.add(*Package.objects.filter(is_default=True))
            user.save()

            token = Token(player=user, uuid=uuid4())
            token.save()

            login(request, user)
            return redirect('/accounts/profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})
