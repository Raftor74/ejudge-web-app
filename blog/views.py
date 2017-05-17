from django.shortcuts import render
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
    if request.user:
        user_role = str(request.user)
    else:
        user_role = "No data"
    return render(request, 'blog/ejudge.html',{'role':user_role})

def test(request):

    return render(request, 'blog/test.html')

def ejudgelogin(request):
    error = ''
    user_id = 0
    if request.method == 'POST':
        if request.POST['do_login']:
            login = request.POST['login']
            password = request.POST['password']
            callback = EjudgeUser.check_ejudge_user(login,password)
            if callback['error'] != '':
                error = callback['error']
            else:
                user_id = callback['data']
    return render(request, 'blog/ejudge_login.html',{'error':error})
