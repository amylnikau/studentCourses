from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.contrib.auth import login
from django.views.generic import FormView

from courses.forms import LoginForm


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

