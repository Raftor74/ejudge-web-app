from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.ejudge import EjudgeUser

# Create your views here.
from blog.models import News


def index (request):
    return render(request, 'blog/index.html')

def news(request):
    #Получаем все новости
    allNews = News.objects.all().order_by("-time")

    #Передаём их в шаблон
    context = {
        'news': allNews,
    }
    return render(request, 'blog/news.html', context)

def about(request):
    return render(request, 'blog/about.html')

def ejudge(request):
    user_data = ''
    if ('user_id' not in request.session) and (str(request.user) != 'admin'):
        return redirect('/ejudgelogin/')
    else:
        if ('user_id' in request.session):
            user_id = request.session['user_id']
            user_data = EjudgeUser.get_user_by_id(user_id)
            if(user_data['error']):
                user_data = ''
            else:
                user_data = user_data['data']

    if request.user:
        user_role = str(request.user)
    else:
        user_role = "No data"
    return render(request, 'blog/ejudge.html',{'role':user_role,'user_data':user_data})

def test(request):
    return redirect('/')

def ejudgelogout(request):
    if ('user_id' in request.session):
        del request.session['user_id']
        request.session.modified = True
        return redirect('/')
    else:
        return redirect('/')

def ejudgeaction(request):
    if request.method == 'POST':
        if 'action' in request.POST:
            answer = EjudgeUser.do_control_action(request.POST['action'])
            return HttpResponse(answer, content_type='text/html')
        else:
            return HttpResponse('Bad Data', content_type='text/html')
    else:
        return HttpResponse('Bad Data', content_type='text/html')

def ejudgelogin(request):
    if ('user_id' in request.session):
        return redirect('/ejudgeservice/')

    error_login = ''
    error_register = ''
    user_id = 0
    if request.method == 'POST':
        if 'do_login' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            callback = EjudgeUser.check_ejudge_user(login,password)
            if callback['error'] != '':
                error_login = callback['error']
            else:
                user_id = callback['data']
                request.session.set_expiry(3600)
                request.session['user_id'] = user_id
                request.session.modified = True
                return redirect('/ejudgeservice/')


        elif 'do_register' in request.POST:
            login = request.POST['reg_login']
            password = request.POST['reg_password']
            password_confirm = request.POST['reg_password_2']
            email = request.POST['reg_email']
            error = EjudgeUser.validate_user_data(login,password,password_confirm,email)
            if len(error) != 0:
                error_register = error
            else:
                error = EjudgeUser.check_user_exist(login,password,email)
                if len(error['error']) != 0:
                    error_register = error['error']
                elif (error['data']):
                    error_register = 'Пользователь с такими данными уже существует'
                else:
                    error = EjudgeUser.registration(login,email,password)
                    if len(error['error']) != 0:
                        error_register = error['error']

    return render(request, 'blog/ejudge_login.html',{'error_login':error_login,'error_register':error_register})
