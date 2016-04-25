from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractUser as AbstractBaseUser
from django.db import models
from django_enumfield import enum


USER_TYPE_MODELS = ['Student', 'Professor']


class DepartmentChoices(enum.Enum):
    FAMCS = 0
    MMF = 1

    labels = {
        FAMCS: _('Faculty of Applied Mathematics and Computer Science'),
        MMF: _('Mechanics and Mathematics Faculty')
    }


class PostChoices(enum.Enum):
    ACADEMICIAN = 0
    PROFESSOR = 1
    DOCENT = 2

    labels = {
        ACADEMICIAN: _('Academician'),
        PROFESSOR: _('Professor'),
        DOCENT: _('Docent')
    }


class YearChoices(enum.Enum):
    FIRST_YEAR = 1
    SECOND_YEAR = 2
    THIRD_YEAR = 3
    FORTH_YEAR = 4
    FIFTH_YEAR = 5

    labels = {
        FIRST_YEAR: '1',
        SECOND_YEAR: '2',
        THIRD_YEAR: '3',
        FORTH_YEAR: '4',
        FIFTH_YEAR: '5'
    }


class AbstractUser(AbstractBaseUser):
    user_type = models.ForeignKey(ContentType, null=True, editable=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Professor(User):
    post = enum.EnumField(PostChoices, verbose_name=_('post'), default=PostChoices.DOCENT)
    department = enum.EnumField(DepartmentChoices, verbose_name=_('department'), default=DepartmentChoices.FAMCS)

    class Meta:
        verbose_name = 'Professor'


class Student(User):
    year_in_university = enum.EnumField(YearChoices, verbose_name=_('year'), default=YearChoices.FIRST_YEAR)
    group = models.IntegerField(_('group'))
    department = enum.EnumField(DepartmentChoices, verbose_name=_('department'), default=DepartmentChoices.FAMCS)
    courses = models.ManyToManyField('CourseOffering')

    class Meta:
        verbose_name = 'Student'


class CourseOffering(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    prerequisites = models.TextField(_('prerequisites'), max_length=500, blank=True)


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_mark = models.IntegerField(_('first mark'), null=True)
    second_mark = models.IntegerField(_('second mark'), null=True)
    third_mark = models.IntegerField(_('third mark'), null=True)
    forth_mark = models.IntegerField(_('forth mark'), null=True)
