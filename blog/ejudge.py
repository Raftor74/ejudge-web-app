from django.db import connection, connections
import hashlib
import subprocess

#Class for Ejudge System
class EjudgeUser:
    def __init__(self,
                user_id = 0,
                login = "",
                email="",
                pwdmethod=0,
                password="",
                privileged=0,
                invisible=0,
                banned=0,
                locked=0,
                readonly=0,
                neverclean=0,
                simplereg=0,
                regtime=0,
                logintime=0,
                pwdtime=0,
                changetime=0):
         #идентификатор пользователя > 0
        self.user_id = user_id
        #login пользователя
        self.login = login
        #e-mail
        self.email = email
        #Способ шифрования 0 - plain, 1 - base64, 2 - sha1
        self.pwdmethod = pwdmethod
        #Пароль
        self.password = password
        #Глобальная привелегилированость
        self.privileged = privileged
        #глобальная невидимость
        self.invisible = invisible
        #глобальная заблокированность
        self.banned = banned
        #глобальная фиксированность
        self.locked = locked
        #модификация запрещена
        self.readonly = readonly
        #никогда не очищать из БД
        self.neverclean = neverclean
        #создан по процедуре упрощенной регистрации
        self.simplereg = simplereg
        #время регистрации
        self.regtime = regtime
        #время последнего входа
        self.logintime = logintime
        #время последней смены регистрационного пароля
        self.pwdtime = pwdtime
        #время последней смены регистрационного пароля
        self.changetime = changetime

    #Get users from ejudge system
    #return list or string
    def get_users():
        error = ""
        users_list = []
        try:
            ejudge_db = connections['ejudge'].cursor()
        except Exception:
            error = "Cannot connect to database"
            return {'data':users_list,'error':error}
        try:
            ejudge_db.execute("SELECT * FROM logins")
        except Exception:
            error = "Error in SQL Query"
            return {'data':users_list,'error':error}          
        try:
            users = ejudge_db.fetchall()
            for user in users:
                one_user = EjudgeUser(*user)
                users_list.append(one_user)
            return {'data':users_list,'error':error}
        except Exception:
            error = "Cannot get data from database"
            return {'data':users_list,'error':error}

    def get_user_by_id(id):
        error = ""
        try:
            esc_id = int(id)
        except Exception:
            error = "Cannot parse User ID"
            return {'data':'','error':error}
        try:
            ejudge_db = connections['ejudge'].cursor()
        except Exception:
            error = "Cannot connect to database"
            return {'data':'','error':error}
        try:
            sql = "SELECT * FROM logins WHERE user_id = %s"
            data = (str(id))
            ejudge_db.execute(sql,data)
        except Exception:
            error = "Error in SQL Query"
            return {'data':'','error':error}
        try:
            user = EjudgeUser(*ejudge_db.fetchone())
            return {'data':user,'error':error}
        except Exception:
            error = "Cannot load User"
            return {'data':'','error':error}
    
    #Проверяет существует ли пользователь
    def check_ejudge_user(login,password):
        error = ''
        _login = str(login)
        _password = str(password)
        _password = EjudgeUser.get_SHA1_pass(_password)
        try:
            ejudge_db = connections['ejudge'].cursor()
        except Exception:
            error = "Cannot connect to database"
            return {'data':False,'error':error}
        try:
            sql = "SELECT user_id FROM logins WHERE login = %s AND pwdmethod = 2 AND password = %s"
            data = (_login,_password)
            ejudge_db.execute(sql,data)
        except Exception:
            error = "Error in SQL Query. Check ejudge user"
            return {'data':False,'error':error}
        try:
            user_id = ejudge_db.fetchone()[0]
            return {'data':user_id,'error':error}
        except Exception:
            error = "Неверная пара логин / пароль"
            return {'data':False,'error':error}
    
    #Валидация данных пользователя
    def validate_user_data(login,password,password_again,email):
        error = []
        if len(login) < 5 or len(login) > 30:
            error.append("Логин должен быть от 5 до 30 символов")
        if len(password) < 5 or len(password) > 30:
            error.append("Пароль должен быть от 5 до 30 символов")
        if password != password_again:
            error.append("Пароли не совпадают")
        if len(email) == 0:
            error.append("E-mail не может быть пустым")
        return error

    #Регистрирует пользователя
    def registration(login,email,password):
        _login = str(login)
        _password = str(password)
        _password = EjudgeUser.get_SHA1_pass(_password)
        _email = str(email)
        error=''
        try:
            ejudge_db = connections['ejudge'].cursor()
        except Exception:
            error = "Cannot connect to database"
            return {'data':False,'error':error}
        try:
            sql = "INSERT INTO logins (login,email,pwdmethod,password,neverclean) VALUES (%s,%s,2,%s,1)"
            data = (_login,_email,_password)
            ejudge_db.execute(sql,data)
            return {'data':True,'error':error}
        except Exception:
            error = "Error in SQL Query. Register function"
            return {'data':False,'error':error}

    #Проверяет сущ ли пользователь перед регистрацией
    def check_user_exist(login,password,email):
        _login = str(login)
        _password = str(password)
        _password = EjudgeUser.get_SHA1_pass(_password)
        _email = str(email)
        error=''
        try:
            ejudge_db = connections['ejudge'].cursor()
        except Exception:
            error = "Cannot connect to database"
            return {'data':False,'error':error}
        try:
            sql = "SELECT user_id FROM logins WHERE login = %s AND pwdmethod = 2 AND password = %s OR email = %s"
            data = (_login,_password,_email)
            ejudge_db.execute(sql,data)
        except Exception:
            error = "Error in SQL Query. Check_user_exist"
            return {'data':False,'error':error}
        try:
            user_id = ejudge_db.fetchone()[0]
            return {'data':True,'error':error}
        except Exception:
            return {'data':False,'error':error}

    #Return string hashed by SHA-1
    def get_SHA1_pass(string):
        preparestr = string.encode('utf-8')
        return hashlib.sha1(preparestr).hexdigest()
    
    def reload_ejudge_system():
        subprocess.call('/home/ejudge/inst-ejudge/bin/ejudge-control stop', shell=True)
        subprocess.call('/home/ejudge/inst-ejudge/bin/ejudge-control start', shell=True)
