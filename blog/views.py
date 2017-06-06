from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.ejudge import EjudgeUser
from blog.contests import EjudgeContests

# Create your views here.
from blog.models import News, Course, Lesson

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
    return render(request, 'blog/ejudge.html',{'user_data':user_data})

def test(request):
    return render(request, 'blog/test.html')

def courses_list(request):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/ejudgelogin/')
    courses = Course.objects.all()
    return render(request, 'blog/courses_list.html',{'courses':courses})

def courses_detail(request,slug):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/ejudgelogin/')
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'blog/course_detail.html',{'course':course,'lessons':lessons})

def lesson_detail(request,**kwargs):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/ejudgelogin/')
    course = get_object_or_404(Course, slug=kwargs.get('course'))
    lesson = get_object_or_404(Lesson, course=course, slug=kwargs.get('slug'))
    return render(request, 'blog/lesson_detail.html',{'course':course,'lesson':lesson})

def contests(request):
    if 'user_id' not in request.session:
        return redirect('/ejudgelogin/')
    user_id = request.session['user_id']
    #AJAX action
    if request.method == 'POST':
        if 'contest_id' in request.POST:
            contest_id = request.POST['contest_id']
            if not EjudgeContests.register_exist(user_id,contest_id):
                error = EjudgeContests.register_to_contest(user_id,contest_id)['error']
                return HttpResponse(error, content_type='text/html')
    user_contests_ids = EjudgeContests.get_user_contest(user_id)['data']
    avaliable_contests = EjudgeContests.get_contests_data(user_contests_ids,False)
    used_contests = EjudgeContests.get_contests_data(user_contests_ids,True)
    return render(request, 'blog/contests.html',{'avaliable':avaliable_contests,'used':used_contests})

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
