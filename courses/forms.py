from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django.contrib.auth.forms import AuthenticationForm
from django.forms import BooleanField, CheckboxInput


class LoginForm(AuthenticationForm):
    remember_me = BooleanField(required=False, widget=CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.layout = Layout(
            HTML('<h2 class="form-signin-heading">Please sign in</h2>'),
            'username',
            'password',
            'remember_me',
            Submit('sign_in', 'Sign in', css_class='btn btn-lg btn-primary btn-block')
        )

    def clean(self):
        if not self.cleaned_data.get('remember-me'):
            self.request.session.set_expiry(0)
        super().clean()
