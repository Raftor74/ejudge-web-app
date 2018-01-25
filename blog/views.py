from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.models import *


# Главная страница
def index(request):
    return render(request, 'blog/index.html')


# Новости сайта
def news(request):
    news = News.objects.all().order_by("-time")
    return render(request, 'blog/news.html', {'news':news})


# О нас
def about(request):
    return render(request, 'blog/about.html')


"""def ejudgeusers(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user_id = request.POST['user_id']
            if user_id != 1:
                try:
                    user_to_delete = Logins.objects.get(user_id=user_id)
                except:
                    return HttpResponse("error", content_type='text/html')
            user_to_delete.delete()
            return HttpResponse("ok", content_type='text/html')
    users = Logins.objects.all()
    return render(request, 'blog/ejudge_users.html', {'user_data': users})"""


"""def ejudge(request):
    user_data = ''
    if ('user_id' not in request.session) and (str(request.user) != 'admin'):
        return redirect('/')
    else:
        if ('user_id' in request.session):
            user_id = request.session['user_id']
            try:
                user_data = Logins.objects.get(user_id=user_id)
            except:
                user_data = ''
    return render(request, 'blog/ejudge.html', {'user_data': user_data})"""

# Тест страница
def test(request):
    return render(request, 'blog/test.html')

# Список курсов
def courses_list(request):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/')
    courses = Course.objects.all()
    return render(request, 'blog/courses_list.html', {'courses': courses})

# Курс детально
def courses_detail(request, slug):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/')
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'blog/course_detail.html', {'course': course, 'lessons': lessons})

# Урок детально
def lesson_detail(request, **kwargs):
    if 'user_id' not in request.session and not request.user.is_authenticated():
        return redirect('/')
    course = get_object_or_404(Course, slug=kwargs.get('course'))
    lesson = get_object_or_404(Lesson, course=course, slug=kwargs.get('slug'))
    return render(request, 'blog/lesson_detail.html', {'course': course, 'lesson': lesson})


"""def contests(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    # AJAX action
    if request.method == 'POST':
        if 'contest_id' in request.POST and 'delete_contest' not in request.POST:
            contest_id = request.POST['contest_id']
            if not register_exist(user_id, contest_id):
                callback = register_to_contest(user_id, contest_id)
                return HttpResponse(callback, content_type='text/html')
        if 'delete_contest' in request.POST:
            contest_id = request.POST['contest_id']
            if delete_contests(user_id, contest_id):
                return HttpResponse("ok", content_type='text/html')
    user_contests_ids = get_user_contests(user_id)
    avaliable_contests = get_contests_data(user_contests_ids, False)
    used_contests = get_contests_data(user_contests_ids, True)
    return render(request, 'blog/contests.html', {'avaliable':avaliable_contests, 'used':used_contests})"""


"""def ejudgeaction(request):
    if request.method == 'POST':
        if 'action' in request.POST:
            answer = EjudgeUser.do_control_action(request.POST['action'])
            return HttpResponse(answer, content_type='text/html')
        else:
            return HttpResponse('Bad Data', content_type='text/html')
    else:
        return HttpResponse('Bad Data', content_type='text/html')"""
