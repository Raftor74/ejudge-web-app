from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from blog.models import *
from users.classes import UserHelper

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

# Список курсов
def courses_list(request):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))
    courses = Course.objects.all()
    return render(request, 'blog/courses_list.html', {'courses': courses})

# Курс детально
def courses_detail(request, slug):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'blog/course_detail.html', {'course': course, 'lessons': lessons})

# Урок детально
def lesson_detail(request, **kwargs):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))
    course = get_object_or_404(Course, slug=kwargs.get('course'))
    lesson = get_object_or_404(Lesson, course=course, slug=kwargs.get('slug'))
    return render(request, 'blog/lesson_detail.html', {'course': course, 'lesson': lesson})