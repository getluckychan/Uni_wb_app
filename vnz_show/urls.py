from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/student/<user_id>', SignUpStudentView.as_view(), name='sign_up_student'),
    path('signup/educator/<user_id>', SignUpEducatorView.as_view(), name='sign_up_educator'),
    # path('user/<int:user_id>/', profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout_url'),
    path('myprofile/', MyProfileView.as_view(), name='my_profile'),
    path('searchuser/<str:search_data>', SearchUserView.as_view(), name='search_user'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('declined/', declined_area, name='declined_area'),
    path('createtest/', CreateTestView.as_view(), name='create_test'),
    path('setmark/', CreateMarkView.as_view(), name='set_marks'),
    path('createtest/createtask/<test_id>', CreateTaskView.as_view(), name='create_task'),
    path('createtest/createtask/createanswer/<task_id>', CreateAnswerView.as_view(), name='create_answer'),
    path('showtests/', ShowTestsView.as_view(), name="show_tests"),
    path('marks/', get_marks_for_student, name="marks"),
    path('courses/', get_courses_for_student, name="courses"),
    # path('user/setup/<int:user_id>', user_setup, name='user_setup'),
]

