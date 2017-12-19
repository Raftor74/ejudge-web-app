"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,  name='index'),
    url(r'^news/$', views.news,  name='news'),
    url(r'^about-us/$', views.about,  name='about'),
    url(r'^ejudgeservice/$', views.ejudge,  name='ejudge'),
    url(r'^auth/login/$', views.login,  name='login'),
    url(r'^auth/register/$', views.register,  name='register'),
    url(r'^auth/logout/$', views.logout,  name='logout'),
    url(r'^ejudgeaction/$', views.ejudgeaction,  name='ejudgeaction'),
    url(r'^ejudgeusers/$', views.ejudgeusers,  name='ejudgeusers'),
    url(r'^test/$', views.test,  name='test'),
    url(r'^contests/$', views.contests,  name='contests'),
    url(r'^courses/$', views.courses_list,  name='courses_list'),
    url(r'^courses/(?P<slug>\w+)/$', views.courses_detail,  name='courses_detail'),
    url(r'^courses/(?P<course>\w+)/lessons/(?P<slug>\w+)/$', views.lesson_detail,  name='lesson_detail')
]
