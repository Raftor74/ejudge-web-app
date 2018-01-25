from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,  name='index'),
    url(r'^news/$', views.news,  name='news'),
    url(r'^about-us/$', views.about,  name='about'),
    #url(r'^ejudgeservice/$', views.ejudge,  name='ejudge'),
    #url(r'^ejudgeaction/$', views.ejudgeaction,  name='ejudgeaction'),
    #url(r'^ejudgeusers/$', views.ejudgeusers,  name='ejudgeusers'),
    url(r'^test/$', views.test,  name='test'),
    #url(r'^contests/$', views.contests,  name='contests'),
    url(r'^courses/$', views.courses_list,  name='courses_list'),
    url(r'^courses/(?P<slug>\w+)/$', views.courses_detail,  name='courses_detail'),
    url(r'^courses/(?P<course>\w+)/lessons/(?P<slug>\w+)/$', views.lesson_detail,  name='lesson_detail')
]
