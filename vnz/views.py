from django.shortcuts import render
from vnz_show.utils import menu_not_login
from vnz.serializers import *
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponseNotFound, HttpResponse
from vnz_show.forms import *


class UserStudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = UserStudentModelSerializer


class SpecialityViewSet(ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialityModelSerializer


class UserEducatorViewSet(ModelViewSet):
    queryset = Educator.objects.all()
    serializer_class = UserEducatorModelSerializer


class ListOfSubjectsViewSet(ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = ListOfSubjectsModelSerializer


class MarksViewSet(ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksModelSerializer


class RankViewSet(ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankModelSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentModelSerializer


class GroupsViewSet(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsModelSerializer


class ListOfStudentPerGroupViewSet(ModelViewSet):
    queryset = ListOfStudentPerGroup.objects.all()
    serializer_class = ListOfStudentPerGroupModelSerializer


class ListOfUsersViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = ListOfUsersSerializer


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class StudentTestViewSet(ModelViewSet):
    queryset = StudentTest.objects.all()
    serializer_class = StudentTestSerializer


class UnistuffViewSet(ModelViewSet):
    queryset = Unistuff.objects.all()
    serializer_class = UnistuffSerializer


class SpecialityInDepartmentViewSet(ModelViewSet):
    queryset = SpecialityInDepartment.objects.all()
    serializer_class = SpecialityInDepartmentSerializer


class SubjectInSpecialityViewSet(ModelViewSet):
    queryset = SubjectForSpeciality.objects.all()
    serializer_class = SubjectForSpecialitySerializer


def page_not_found(request, exception):
    context = {
        'menu': menu_not_login,
        'title': '404 page not found'
    }
    return render(request, 'errors/404.html', context=context)
