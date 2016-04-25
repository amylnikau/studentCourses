from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^student/(?P<id>[\w.@+-])+', views.student_profile, name='student_profile'),
    url(r'^professor/(?P<id>[\w.@+-])+', views.professor_profile, name='professor_profile')
]
