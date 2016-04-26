from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from courses.forms import UserCreationForm
from courses.models import Professor, Student, User


class UserModelFilter(admin.SimpleListFilter):
    """
    An admin list filter for the UserAdmin which enables
    filtering by its child models.
    """
    title = _('user type')
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        user_types = set([user.user_type for user in model_admin.model.objects.all()])
        return [(user_type.id, user_type.name) for user_type in user_types]

    def queryset(self, request, queryset):
        try:
            value = int(self.value())
        except TypeError:
            value = None

        if value:
            return queryset.filter(user_type_id__exact=value)
        else:
            return queryset


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_filter = (UserModelFilter, 'is_staff', 'is_superuser', )


@admin.register(Professor)
class ProfessorUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'post', 'department', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'post', 'department', 'email')}),
    )

    list_display = ('username', 'first_name', 'last_name', 'post', 'department')
    list_filter = ('post', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('department', 'post', 'first_name', 'last_name')

    add_form = UserCreationForm


@admin.register(Student)
class StudentUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'year_in_university', 'group', 'department', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'year_in_university', 'group', 'department', 'email')}),
    )

    list_display = ('username', 'first_name', 'last_name', 'year_in_university', 'group')
    list_filter = ('year_in_university',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('year_in_university', 'group', 'first_name', 'last_name')

    add_form = UserCreationForm
