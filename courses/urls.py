from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^student/(?P<id>[\w.@+-])+', views.student_profile, name='student_profile'),
    url(r'^professor/select', views.SelectCoursesView.as_view(), name='select_courses'),
    url(r'^professor/put-marks', views.PutMarksView.as_view(), name='put_marks'),
    url(r'^professor/(?P<id>[\w.@+-])+', views.professor_profile, name='professor_profile'),
]
