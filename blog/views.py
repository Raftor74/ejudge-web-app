from django.shortcuts import render
from . import functions

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
    return render(request, 'blog/ejudge.html')

def test(request):
    users = functions.getLoginsFromEjudge()
    password = functions.getSHA1Pass("ejudge")
    return render(request, 'blog/test.html', {'users':users,'pass':password})
