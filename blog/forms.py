from django import forms
from django.core.exceptions import ObjectDoesNotExist
from blog.models import Logins
from blog.functions import *


class LoginForm(forms.Form):
    # Виджеты для полей
    login_widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter login'})
    password_widget = forms.PasswordInput(render_value=False,
                                          attrs={'class': 'form-control', 'placeholder': 'Enter password'})

    # Данные
    login = forms.CharField(widget=login_widget, label='Ваш логин', error_messages={'required': 'Введите логин'},
                            max_length=30)
    password = forms.CharField(widget=password_widget, label='Ваш пароль',
                               error_messages={'required': 'Введите пароль'}, max_length=200)

    # Валидация логина
    def clean_login(self):
        login = self.cleaned_data['login']
        return login

    # Валидация пароля
    def clean_password(self):
        password = self.cleaned_data['password']
        password = getSHA1Pass(password)
        return password

    # Общая валидация
    def clean(self):
        data = super().clean()
        return data


class RegisterForm(forms.Form):
    # Виджеты для полей
    login_widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter login'})
    password_widget = forms.PasswordInput(render_value=False,
                                          attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    password_again_widget = forms.PasswordInput(render_value=False,
                                                attrs={'class': 'form-control', 'placeholder': 'Enter password again'})
    email_widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})

    # Данные
    login = forms.CharField(widget=login_widget, label='Ваш логин', error_messages={'required': 'Введите логин'},
                            max_length=30)
    password = forms.CharField(widget=password_widget, label='Ваш пароль',
                               error_messages={'required': 'Введите пароль'}, max_length=200)
    password_again = forms.CharField(widget=password_again_widget, label='Ваш пароль ещё раз',
                                     error_messages={'required': 'Введите пароль'}, max_length=200)
    email = forms.EmailField(widget=email_widget, label='Ваш E-mail', error_messages={'required': 'Введите пароль'},
                             max_length=200)

    # Валидация логина
    def clean_login(self):
        login = self.cleaned_data['login']
        if len(login) < 5 or len(login) > 30:
            raise forms.ValidationError("Логин должен быть от 5 до 30 символов")
        return login

    # Валидация пароля
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5 or len(password) > 30:
            raise forms.ValidationError("Пароль должен быть от 5 до 30 символов")
        password = getSHA1Pass(password)
        return password

    # Валидация повторного пароля
    def clean_password_again(self):
        password_again = self.cleaned_data['password_again']
        password_again = getSHA1Pass(password_again)
        return password_again

    # Валидация email
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    # Общая валидация
    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_again = data.get('password_again')
        if password != password_again:
            raise forms.ValidationError("Пароли не совпадают")
        return data
