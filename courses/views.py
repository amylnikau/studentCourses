from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url, get_object_or_404
from django.contrib.auth import login
from django.views.generic import FormView, TemplateView
from extra_views import InlineFormSetView

from courses.forms import LoginForm, CourseOfferingFormSet, \
    CourseOfferingFormSetHelper, CourseOfferingForm
from courses.models import CourseOffering, Course, Professor


def index(request):
    return render(request, 'courses/index.html')


@login_required
def student_profile(request, id):
    return render(request, 'courses/student_profile.html', {'user': request.user})


@login_required
def professor_profile(request, id):
    return render(request, 'courses/professor_profile.html', {'user': request.user})


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            redirect_to = self.get_redirect_url(user)
            return HttpResponseRedirect(redirect_to)
        else:
            return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        redirect_to = self.get_redirect_url(user)
        login(self.request, user)
        return HttpResponseRedirect(redirect_to)

    def get_redirect_url(self, user):
        if user.user_type.name == 'Professor':
            redirect_to = reverse('courses:professor_profile', args=(user.username,))
        elif user.user_type.name == 'Student':
            redirect_to = reverse('courses:student_profile', args=(user.username,))
        else:
            redirect_to = resolve_url(settings.LOGIN_URL)
        return redirect_to


class SelectCoursesView(InlineFormSetView):
    model = Professor
    inline_model = CourseOffering
    form_class = CourseOfferingForm
    template_name = 'courses/professor_select_courses.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Professor, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        data = super(SelectCoursesView, self).get_context_data(**kwargs)
        data['helper'] = CourseOfferingFormSetHelper()
        data['user_id'] = self.request.user.id
        professor_courses = CourseOffering.objects.all().values_list('course_title', flat=True)
        data['courses'] = Course.objects.all().exclude(course_title__in=list(professor_courses)).values_list('course_title', flat=True)
        if self.request.POST:
            data['formset'] = CourseOfferingFormSet(self.request.POST)
        else:
            data['formset'] = CourseOfferingFormSet(instance=self.request.user)
        return data


class PutMarksView(TemplateView):
    template_name = 'courses/professor_put_marks.html'
