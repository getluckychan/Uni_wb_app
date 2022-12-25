from .views import *
from rest_framework.routers import DefaultRouter

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



urlpatterns = router.urls
