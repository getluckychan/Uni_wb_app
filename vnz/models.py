from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import *
from django.contrib.auth.models import Permission


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    is_student = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)
    is_unistuff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    REQUIRED_FIELDS = ['full_name',
                       'date_of_birth',
                       ]

    USERNAME_FIELD = 'email'
    username = None

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Student(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE, null=True, unique=False)
    acception = models.DateField(unique=False)
    graduation = models.DateField(unique=False)

    class Meta:
        permissions = (
            ('can_view_student', 'Can view student'),
            ('can_edit_student', 'Can edit student'),
            ('can_delete_student', 'Can delete student'),
            ('can_add_student', 'Can add student'),
        )

    def __str__(self):
        return self.user.full_name


class Educator(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE, unique=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, unique=False)
    acception = models.DateField()

    class Meta:
        permissions = (
            ('can_view_educator', 'Can view educator'),
            ('can_edit_educator', 'Can edit educator'),
            ('can_delete_educator', 'Can delete educator'),
            ('can_add_educator', 'Can add educator'),
        )

    def __str__(self):
        return self.user.full_name


class Unistuff(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.full_name


class Speciality(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        permissions = (
            ('can_view_speciality', 'Can view speciality'),
            ('can_edit_speciality', 'Can edit speciality'),
            ('can_delete_speciality', 'Can delete speciality'),
            ('can_add_speciality', 'Can add speciality'),
        )

    def __str__(self):
        return self.title


class Subjects(models.Model):
    subject_name = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ('can_view_subjects', 'Can view subjects'),
            ('can_edit_subjects', 'Can edit subjects'),
            ('can_delete_subjects', 'Can delete subjects'),
            ('can_add_subjects', 'Can add subjects'),
        )

    def __str__(self):
        return self.subject_name


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, unique=False)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, unique=False)
    mark = models.FloatField()
    setted_by = models.ForeignKey(Educator, on_delete=models.PROTECT, null=True)
    date = models.DateField()

    class Meta:
        permissions = (
            ('can_view_marks', 'Can view marks'),
            ('can_edit_marks', 'Can edit marks'),
            ('can_delete_marks', 'Can delete marks'),
            ('can_add_marks', 'Can add marks'),
        )

    def __str__(self):
        return self.mark


class Rank(models.Model):
    rank = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ('can_view_rank', 'Can view rank'),
            ('can_edit_rank', 'Can edit rank'),
            ('can_delete_rank', 'Can delete rank'),
            ('can_add_rank', 'Can add rank'),
        )

    def __str__(self):
        return self.rank


class Department(models.Model):
    department = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ('can_view_department', 'Can view department'),
            ('can_edit_department', 'Can edit department'),
            ('can_delete_department', 'Can delete department'),
            ('can_add_department', 'Can add department'),
        )

    def __str__(self):
        return self.department


class Groups(models.Model):
    class Course(models.TextChoices):
        FIRST = '1', _('1')
        SECOND = '2', _('2')
        THIRD = '3', _('3')
        FOURTH = '4', _('4')

    course = models.CharField(
        max_length=50,
        choices=Course.choices,
        default=Course.FIRST
    )
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, unique=False)
    group_number = models.IntegerField(unique=False)
    curator = models.ForeignKey(Educator, on_delete=models.CASCADE, unique=False, null=True)

    class Meta:
        permissions = (
            ('can_view_groups', 'Can view groups'),
            ('can_edit_groups', 'Can edit groups'),
            ('can_delete_groups', 'Can delete groups'),
            ('can_add_groups', 'Can add groups'),
        )

    def __str__(self):
        return self.group_number and self.course


class ListOfStudentPerGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_listofstudentpergroup', 'Can view listofstudentpergroup'),
            ('can_edit_listofstudentpergroup', 'Can edit listofstudentpergroup'),
            ('can_delete_listofstudentpergroup', 'Can delete listofstudentpergroup'),
            ('can_add_listofstudentpergroup', 'Can add listofstudentpergroup'),
        )


class Message(models.Model):
    text = models.CharField(max_length=255, unique=False)

    class Meta:
        permissions = (
            ('can_view_message', 'Can view message'),
            ('can_edit_message', 'Can edit message'),
            ('can_delete_message', 'Can delete message'),
            ('can_add_message', 'Can add message'),
        )

    def __str__(self):
        return self.text


class SpecialityInDepartment(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_specialityindepartment', 'Can view specialityindepartment'),
            ('can_edit_specialityindepartment', 'Can edit specialityindepartment'),
            ('can_delete_specialityindepartment', 'Can delete specialityindepartment'),
            ('can_add_specialityindepartment', 'Can add specialityindepartment'),
        )

    def __str__(self):
        return self.speciality and self.department


class SubjectForSpeciality(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_subjectforspeciality', 'Can view subjectforspeciality'),
            ('can_edit_subjectforspeciality', 'Can edit subjectforspeciality'),
            ('can_delete_subjectforspeciality', 'Can delete subjectforspeciality'),
            ('can_add_subjectforspeciality', 'Can add subjectforspeciality'),
        )

    def __str__(self):
        return self.subject and self.speciality


class Test(models.Model):
    theme = models.CharField(max_length=150, unique=False)
    author = models.ForeignKey(Educator, on_delete=models.CASCADE, unique=False)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, unique=False)
    time = models.DurationField(unique=False)
    date = models.DateField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, unique=False)

    class Meta:
        permissions = (
            ('can_view_test', 'Can view test'),
            ('can_edit_test', 'Can edit test'),
            ('can_delete_test', 'Can delete test'),
            ('can_add_test', 'Can add test'),
        )

    def __str__(self):
        return self.theme and self.author


class Task(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, unique=False)
    question = models.CharField(max_length=500, unique=False)

    class Meta:
        permissions = (
            ('can_view_task', 'Can view task'),
            ('can_edit_task', 'Can edit task'),
            ('can_delete_task', 'Can delete task'),
            ('can_add_task', 'Can add task'),
        )

    def __str__(self):
        return self.question


class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
    answer = models.CharField(max_length=150, unique=False)
    correctness = models.BooleanField(unique=False)

    class Meta:
        permissions = (
            ('can_view_answer', 'Can view answer'),
            ('can_edit_answer', 'Can edit answer'),
            ('can_delete_answer', 'Can delete answer'),
            ('can_add_answer', 'Can add answer'),
        )

    def __str__(self):
        return self.answer


class StudentTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, unique=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, unique=False)
    mark = models.FloatField(unique=False)
    date = models.DateField(unique=False)

    class Meta:
        permissions = (
            ('can_view_studenttest', 'Can view studenttest'),
            ('can_edit_studenttest', 'Can edit studenttest'),
            ('can_delete_studenttest', 'Can delete studenttest'),
            ('can_add_studenttest', 'Can add studenttest'),
        )

    def __str__(self):
        return self.student and self.test

