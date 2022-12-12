from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.db import transaction
from vnz.models import *


# FIXME: fix forms for sign in and sign up beside new users models
class RegistrationForm(forms.Form):
    JOBS = (
        ("STUDENT", "Student"),
        ("EDUCATOR", "Educator")
    )
    job = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                                  'class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords don`t match"
            )


class StudentSetUpForm(forms.Form):
    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    acception = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                              'class': 'form-control', }))
    graduation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                               'class': 'form-control', }))


class EducatorSetUpForm(forms.Form):
    rank = forms.ModelChoiceField(
        queryset=Rank.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    acception = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                              'class': 'form-control', }))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class UserSetUp(forms.Form):
    JOBS = (
        ("STUDENT", "Student"),
        ("EDUCATOR", "Educator")
    )
    job = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'class': 'form-control'}))


class CreateTestForm(forms.Form):
    theme = forms.CharField(max_length=150)
    subject = forms.ModelChoiceField(
        queryset=Subjects.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    time = forms.DurationField(widget=forms.TimeInput(attrs={'class': 'form-control',
                                                             'type': 'time'}))


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'


class CreateTaskForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=500)
    correct_answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    incorrect_answers = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=1000)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    correctness = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))


class CreateSpecialitiesForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = '__all__'


class ShowGroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = '__all__'


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = '__all__'


class CreateMarkForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subjects.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mark = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class CreateGroupForm(forms.Form):

    courses = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )

    course = forms.ChoiceField(choices=courses, widget=forms.Select(attrs={'class': 'form-control'}))

    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

