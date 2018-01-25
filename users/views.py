"""В данном файле лежат все views связанные с авторизацией пользователя на сайте"""

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from users.forms import *
from users.models import *


# Если пользователь перешёл на /auth/ перенаправляем его на login
def index(request):
    return redirect('/auth/login/')


# Авторизация
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
                return render(request, 'users/login.html', {'form': form, 'error_login': error_login})
            request.session.set_expiry(3600)
            request.session['user_id'] = user.user_id
            request.session.modified = True
            return redirect('/ejudgeservice/')
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm(auto_id='auth_%s')
        return render(request, 'users/login.html', {'form': form})


# Регистрация
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
                return render(request, 'users/register.html', {'form': form, 'error_reg': error_registration})
            except ObjectDoesNotExist:
                try:
                    new_user = Logins.objects.create(login=login, password=password, email=email, pwdmethod=2)
                except:
                    error_registration = "Неопределённая ошибка регистрации!"
                    return render(request, 'users/register.html', {'form': form, 'error_reg': error_registration})
                request.session.set_expiry(3600)
                request.session['user_id'] = new_user.user_id
                request.session.modified = True
                return redirect('/ejudgeservice/')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm(auto_id='reg_%s')
        return render(request, 'users/register.html', {'form': form})


# Выход
def logout(request):
    if ('user_id' in request.session):
        del request.session['user_id']
        request.session.modified = True
        return redirect('/')
    else:
        return redirect('/')