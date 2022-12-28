from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from vnz_show.utils import menu_not_login
from vnz.serializers import *
from rest_framework.viewsets import ModelViewSet, ViewSet
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


def page_not_found(request, exception):
    context = {
        'menu': menu_not_login,
        'title': '404 page not found'
    }
    return render(request, 'errors/404.html', context=context)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)