from django.http import HttpResponseForbidden, HttpResponseRedirect

from vnz.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic.edit import FormMixin, ProcessFormView

menu_not_login = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Login', 'url_name': 'login'},
    {'title': 'SignUp', 'url_name': 'signup'},
]

menu_student = [
    {'title': 'Courses', 'url_name': 'courses'},
    {'title': 'Marks', 'url_name': 'marks'},
    {'title': 'Chat', 'url_name': 'chat_main'},
]

menu_educator = [
    {'title': 'Create test', 'url_name': 'create_test'},
    {'title': 'Set marks', 'url_name': 'set_marks'},
    {'title': 'Chat', 'url_name': 'chat_main'},
]


def educator_recognizer(educator_pk):
    educator = Educator.objects.get(user_id=educator_pk)
    return educator


def student_recognizer(student_pk):
    student = Student.objects.get(user_id=student_pk)
    return student


class DataMixin:
    def get_user_contex(self, **kwargs):
        contex = kwargs


