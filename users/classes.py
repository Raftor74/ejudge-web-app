import subprocess
from .models import Logins
from django.core.exceptions import ObjectDoesNotExist
from mysite import settings


# Класс для управления системой Ejudge
class EjudgeControl(object):

    # Разбирает запрос для управления системой
    def resolve_action(self, action):
        _action = str(action)
        answer = "Bad action"
        if (_action == 'start'):
            try:
                self.start_ejudge_system()
                answer = "System started"
            except Exception:
                answer = "Error start system"
        if (_action == 'restart'):
            try:
                self.reload_ejudge_system()
                answer = "System reloaded"
            except Exception:
                answer = "Error reload system"
        if (_action == 'stop'):
            try:
                self.stop_ejudge_system()
                answer = "System stopped"
            except Exception:
                answer = "Error stop system"

        return answer

    # Перезагружает систему Ejudge
    def reload_ejudge_system(self):
        subprocess.call(settings.EJUDGE_CONTROL_PATH + ' stop', shell=True)
        subprocess.call(settings.EJUDGE_CONTROL_PATH + ' start', shell=True)

    # Запускает систему Ejudge
    def start_ejudge_system(self):
        subprocess.call(settings.EJUDGE_CONTROL_PATH + ' start', shell=True)

    # Останавливает систему Ejudge
    def stop_ejudge_system(self):
        subprocess.call(settings.EJUDGE_CONTROL_PATH + ' stop', shell=True)


# Класс для работы c пользователем
class UserHelper(object):

    # Возвращает id пользователя
    @staticmethod
    def get_user_id(request):
        if 'user_id' in request.session:
            return request.session['user_id']
        else:
            return None

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