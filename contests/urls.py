from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,  name='contests'),
    url(r'^add/$', views.add,  name='contests_add'),
    url(r'^show/(?P<contest_id>\d+)/$', views.show,  name='contests_show'),
    url(r'^edit/(?P<contest_id>\d+)/$', views.edit,  name='contests_edit'),
    url(r'^list/$', views.contest_list,  name='contests_list'),
    url(r'^getproblemslist/$', views.get_problems_list,  name='contests_get_problem'),
]