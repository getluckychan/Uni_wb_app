from django.template.defaulttags import url
from django.urls import include, path

from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"userstudent", UserStudentViewSet)
router.register(r"usereducator", UserEducatorViewSet)
router.register(r"speciality", SpecialityViewSet)
router.register(r"listofsubject", ListOfSubjectsViewSet)
router.register(r"marks", MarksViewSet)
router.register(r"rank", RankViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"groups", GroupsViewSet)
router.register(r"users", ListOfUsersViewSet)
router.register(r"test", TestViewSet)
router.register(r"task", TaskViewSet)
router.register(r"answers", AnswerViewSet)
router.register(r"message", StudentTestViewSet)
router.register(r"unistuff", UnistuffViewSet)
router.register(r"specialityindepartment", SpecialityInDepartmentViewSet)
router.register(r"subjectforspeciality", SubjectInSpecialityViewSet)

urlpatterns = [path('modules/', include(router.urls)),
               path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               path('register/', RegisterView.as_view(), name='auth_register'),
               path('', getRoutes),
               path('test/', testEndPoint, name='test')
               ]
