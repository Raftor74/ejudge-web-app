from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,  name='problems'),
    url(r'^show/(?P<task_id>\d+)/$', views.show,  name='problems_show'),
    url(r'^edit/(?P<task_id>\d+)/$', views.edit,  name='problems_edit'),
    url(r'^add/$', views.add,  name='problems_add'),
]