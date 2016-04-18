from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import login as contrib_login
from courses.forms import LoginForm


@login_required
def profile(request):
    return render(request, 'courses/profile.html', {'user': request.user})


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login(request, authentication_form=LoginForm, **kwargs)
