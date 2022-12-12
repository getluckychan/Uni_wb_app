from vnz.models import *

menu_not_login = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Login', 'url_name': 'login'},
    {'title': 'SignUp', 'url_name': 'signup'},
]

menu_student = [
    {'title': 'Courses', 'url_name': 'courses'},
    {'title': 'Marks', 'url_name': 'marks'},
    {'title': 'Logout', 'url_name': 'logout_url'},
]

menu_educator = [
    {'title': 'Create test', 'url_name': 'create_test'},
    {'title': 'Set marks', 'url_name': 'set_marks'},
    {'title': 'Logout', 'url_name': 'logout_url'},
]


def educator_recognizer(educator_pk):
    educator = Educator.objects.get(user_id=educator_pk)
    return educator



class DataMixin:
    def get_user_contex(self, **kwargs):
        contex = kwargs

