from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from site_auth.forms import *
from site_auth.models import Logins


# Аутентификация
def login(request):
    if ('user_id' in request.session):
        return redirect('/ejudgeservice/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            try:
                user = Logins.objects.get(login=login, password=password)
            except ObjectDoesNotExist:
                error_login = "Неверные логин или пароль!"
                return render(request, 'site_auth/ejudge_login.html', {'form': form, 'error_login': error_login})
            request.session.set_expiry(3600)
            request.session['user_id'] = user.user_id
            request.session.modified = True
            return redirect('/ejudgeservice/')
        else:
            return render(request, 'site_auth/ejudge_login.html', {'form': form})
    else:
        form = LoginForm(auto_id='auth_%s')
        return render(request, 'site_auth/ejudge_login.html', {'form': form})


def register(request):
    if ('user_id' in request.session):
        return redirect('/ejudgeservice/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = Logins.objects.get(login=login, email=email)
                error_registration = "Пользователь с таким Login и Email уже существует!"
                return render(request, 'site_auth/ejudge_register.html', {'form': form, 'error_reg': error_registration})
            except ObjectDoesNotExist:
                try:
                    new_user = Logins.objects.create(login=login, password=password, email=email, pwdmethod=2)
                except:
                    error_registration = "Неопределённая ошибка регистрации!"
                    return render(request, 'site_auth/ejudge_register.html', {'form': form, 'error_reg': error_registration})
                request.session.set_expiry(3600)
                request.session['user_id'] = new_user.user_id
                request.session.modified = True
                return redirect('/ejudgeservice/')
        else:
            return render(request, 'site_auth/ejudge_register.html', {'form': form})
    else:
        form = RegisterForm(auto_id='reg_%s')
        return render(request, 'site_auth/ejudge_register.html', {'form': form})
# Конец аутентификации


def logout(request):
    if ('user_id' in request.session):
        del request.session['user_id']
        request.session.modified = True
        return redirect('/')
    else:
        return redirect('/')