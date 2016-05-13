from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.forms import BooleanField, CheckboxInput, TextInput, inlineformset_factory
from courses.models import USER_TYPE_MODELS, CourseOffering, Professor


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
        super().clean()
        if self.user_cache and self.user_cache.user_type.name not in USER_TYPE_MODELS:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)


class UserCreationForm(BaseUserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=TextInput(attrs={'size': '25'}))
    last_name = forms.CharField(max_length=30, required=True, widget=TextInput(attrs={'size': '25'}))


class CourseOfferingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_title'].widget.attrs['readonly'] = True
        self.fields['prerequisites'].widget.attrs['rows'] = 1

    class Meta:
        model = CourseOffering
        fields = '__all__'


class CourseOfferingFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CourseOfferingFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_id = 'id_CourseOfferingForm'
        self.form_method = 'post'
        self.template = 'bootstrap4/table_inline_formset.html'
        self.render_required_fields = True


CourseOfferingFormSet = inlineformset_factory(Professor, CourseOffering, extra=0, form=CourseOfferingForm, can_delete=True)
