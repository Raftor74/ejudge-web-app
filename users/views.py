from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from .classes import UserHelper
from users.forms import *

"""В данном файле лежат все views связанные с авторизацией пользователя на сайте"""


# Если пользователь перешёл на /auth/ перенаправляем его на login
def index(request):
    if not UserHelper.is_auth(request) and not UserHelper.is_admin(request):
        return redirect(reverse('login'))
    userinfo = UserHelper.get_user_info(request)
    return render(request, 'users/profile.html', locals())


# Авторизация
def login(request):
    if UserHelper.is_auth(request):
        return redirect(reverse('profile'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            if UserHelper.login(request, login=login, password=password):
                return redirect(reverse('profile'))
            else:
                error_login = "Неверные логин или пароль!"
                return render(request, 'users/login.html', {'form': form, 'error_login': error_login})
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm(auto_id='auth_%s')
        return render(request, 'users/login.html', {'form': form})


# Регистрация
def register(request):
    if UserHelper.is_auth(request):
        return redirect(reverse('profile'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            pwdmethod = 2
            if UserHelper.is_exist(login=login):
                error = "Пользователь с таким Login уже существует!"
                return render(request, 'users/register.html', {'form': form, 'error_reg': error})
            if UserHelper.is_exist(email=email):
                error = "Пользователь с таким Email уже существует!"
                return render(request, 'users/register.html', {'form': form, 'error_reg': error})
            status = UserHelper.register(request, login=login, password=password, email=email, pwdmethod=pwdmethod)
            if status:
                return redirect(reverse('profile'))
            else:
                error = "Неопределенная ошибка регистрации!"
                return render(request, 'users/register.html', {'form': form, 'error_reg': error})
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm(auto_id='reg_%s')
        return render(request, 'users/register.html', {'form': form})


# Выход
def logout(request):
    UserHelper.logout(request)
    return redirect('/')