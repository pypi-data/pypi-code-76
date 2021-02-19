from lavender.forms import EmailChangeForm, QuentaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render

from lavender.models import Quenta


@login_required
def profile(request):
    email_form = EmailChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    quenta = Quenta.objects.filter(player=request.user).first()
    quenta_form = QuentaForm(user=request.user, instance=quenta)

    if request.method == 'POST':
        if request.POST['form'] == 'email':
            email_form = EmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Почта успешно изменена!')
            else:
                for field in email_form:
                    for error in field.errors:
                        messages.error(request, error)

        elif request.POST['form'] == 'password':
            password_form = PasswordChangeForm(data=request.POST, user=request.user)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Пароль успешно изменён!')
            else:
                for field in password_form:
                    for error in field.errors:
                        messages.error(request, error)

        elif request.POST['form'] == 'quenta':
            quenta_form = QuentaForm(data=request.POST, user=request.user, instance=quenta)
            if quenta_form.is_valid():
                quenta_form.save()
                messages.success(request, 'Квента успешно сохранена!')
            else:
                for field in quenta_form:
                    for error in field.errors:
                        messages.error(request, error)

    return render(request, 'profile/profile.html', {
        'user': request.user,
        'history': request.user.loghistory_set.order_by('-id')[:10],
        'quenta': quenta,
        'email_form': email_form,
        'password_form': password_form,
        'quenta_form': quenta_form,
    })
