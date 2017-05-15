from django.db import connection, connections
import hashlib
import urllib.request
import html
import re
 
def getWeather():
    link = "http://pogoda.74.ru/"
    file = urllib.request.urlopen(link)
    data = file.read()
    data = data.decode("UTF-8")
    file.close()
    value = re.findall(r'<span class="value__main">(.*?)</span>', str(data))
    description = re.findall(r'<span class="value-description">(.*?)</span>', str(data))
    weather = {
        'value': html.unescape(str(value[0])),
        'description' : html.unescape(str(description[0])),
    }
    return weather

def getLoginsFromEjudge():
    users_list = []
    try:
        ejudge_db = connections['ejudge'].cursor()
        ejudge_db.execute("SELECT * FROM logins")
        users = ejudge_db.fetchall()
        for user in users:
            one_user = {}
            one_user = {
                #идентификатор пользователя > 0
                'user_id':user[0],
                #login пользователя
                'login':user[1],
                #e-mail
                'email':user[2],
                #Способ шифрования 0 - plain, 1 - base64, 2 - sha1
                'pwdmethod':user[3],
                #Пароль
                'password':user[4],
                #Глобальная привелегилированость
                'privileged':user[5],
                #глобальная невидимость
                'invisible':user[6],
                #глобальная заблокированность
                'banned':user[7],
                #глобальная фиксированность
                'locked':user[8],
                #модификация запрещена
                'readonly':user[9],
                #никогда не очищать из БД
                'neverclean':user[10],
                #создан по процедуре упрощенной регистрации
                'simplereg':user[11],
                #время регистрации
                'regtime':user[12],
                #время последнего входа
                'logintime':user[13],
                #время последней смены регистрационного пароля
                'pwdtime':user[14],
                #время последней смены регистрационного пароля
                'changetime':user[15]
            }
            users_list.append(one_user)
        return users_list

    except Exception:
        return users_list

def getSHA1Pass(string):
    preparestr = string.encode('utf-8')
    return hashlib.sha1(preparestr).hexdigest()

