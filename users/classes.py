from .models import Logins, Users
from django.core.exceptions import ObjectDoesNotExist

""" Класс для работы пользователя """


class UserHelper(object):

    # Возвращает информацию о пользователе
    @staticmethod
    def get_user_info(request):
        try:
            id = request.session['user_id']
        except:
            return False
        try:
            user = Logins.objects.get(user_id=id)
            return user
        except ObjectDoesNotExist:
            return False

    # Проверяет существует ли пользователь
    @staticmethod
    def is_exist(**kwargs):
        if Logins.objects.filter(**kwargs).exists():
            return True
        else:
            return False

    # Проверяет залогиненость
    @staticmethod
    def is_auth(request):
        if 'user_id' in request.session:
            return True
        else:
            return False

    # Проверяет является ли пользователь админом
    @staticmethod
    def is_admin(request):
        if request.user.is_authenticated():
            return True
        else:
            return False

    # Регистрирует пользователя
    @staticmethod
    def register(request, **kwargs):
        try:
            user = Logins.objects.create(**kwargs)
        except:
            return False
        request.session.set_expiry(3600)
        request.session['user_id'] = user.user_id
        request.session.modified = True
        return True

    # Логинимся пользователем
    @staticmethod
    def login(request, **kwargs):
        if UserHelper.is_exist(**kwargs):
            user = Logins.objects.get(**kwargs)
            request.session.set_expiry(3600)
            request.session['user_id'] = user.user_id
            request.session.modified = True
            return True
        else:
            return False

    @staticmethod
    def delete(request, **kwargs):
        try:
            Logins.objects.get(kwargs).delete()
            return True
        except:
            return False


    @staticmethod
    def update(**kwargs):
        pass

    @staticmethod
    def logout(request):
        if UserHelper.is_auth(request):
            del request.session['user_id']
            request.session.modified = True
            return True
        return False