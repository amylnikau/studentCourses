from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login as auth_login
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from courses.forms import LoginForm


def index(request):
    return render(request, 'courses/index.html')


@login_required
def student_profile(request, id):
    return render(request, 'courses/student_profile.html', {'user': request.user})


@login_required
def professor_profile(request, id):
    return render(request, 'courses/professor_profile.html', {'user': request.user})


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user.user_type.name == 'Professor':
                    redirect_to = reverse('courses:professor_profile', args=(user.username,))
                elif user.user_type.name == 'Student':
                    redirect_to = reverse('courses:student_profile', args=(user.username,))
                else:
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
                    return HttpResponseRedirect(redirect_to)

                # Ensure the user-originating redirection url is safe.
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

                # Okay, security check complete. Log the user in.
                auth_login(request, user)

                return HttpResponseRedirect(redirect_to)
        else:
            form = LoginForm(request)
        return TemplateResponse(request, 'registration/login.html', context={'form': form})
