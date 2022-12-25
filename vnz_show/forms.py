from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import transaction
from vnz.models import *
from secrets import compare_digest


class UserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password and job."""
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    JOBS = (
        ("STUDENT", "Student"),
        ("EDUCATOR", "Educator")
    )
    job = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('email', 'full_name', 'avatar', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            # check if user is student or educator
            if self.cleaned_data['job'] == 'STUDENT':
                user.is_student = True
            elif self.cleaned_data['job'] == 'EDUCATOR':
                user.is_educator = True
            user.save()
        return user


class SignUpAsStudentForm(forms.ModelForm):
    # adding new user to student model
    class Meta:
        model = Student
        fields = ('speciality', 'acception', 'graduation')
        widgets = {
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'acception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'graduation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class SignUpAsEducatorForm(forms.ModelForm):
    # adding new user to educator model
    class Meta:
        model = Educator
        fields = ('department', 'rank', 'acception')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
            'acception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class EditMyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email', 'full_name', 'avatar', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self):
        super().__init__()
        self.fields['email'].disabled = True


class EducatorUpdateForm(forms.ModelForm):
    class Meta:
        model = Educator
        fields = ('department', 'rank', 'acception')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
            'acception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('speciality', 'acception', 'graduation')
        widgets = {
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'acception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'graduation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class MyProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('full_name', 'email', 'date_of_birth')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class UserSetUp(forms.Form):
    JOBS = (
        ("STUDENT", "Student"),
        ("EDUCATOR", "Educator")
    )
    job = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'class': 'form-control'}))


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('theme', 'subject', 'time', 'date')
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


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
        fields = ('question',)
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'correctness')
        widgets = {
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'correctness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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


class CreateMarkForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ('student', 'subject', 'mark', 'date')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


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


