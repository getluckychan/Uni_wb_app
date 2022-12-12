from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('<int:user_id>/', index, name='index'),
    path('about/', about, name='about'),
    path('login/', login_in, name='login'),
    path('signup/', register, name='signup'),
    path('signup/student/<int:user_id>/', sign_up_student, name='sign_up_student'),
    path('signup/educator/<int:user_id>/', sign_up_educator, name='sign_up_educator'),
    path('user/<int:user_id>/', profile, name='profile'),
    path('logout/', logout_view, name='logout_url'),
    path('myprofile/', my_profile, name='my_profile'),
    path('declined/', declined_area, name='declined_area'),
    path('createtest/', create_test, name='create_test'),
    path('setmark/', set_marks, name='set_marks'),
    path('createtask/<int:test_id>', create_task, name='create_task'),
    path('chat/', chat_page, name="chat_page"),
    path('showtests/', show_tests, name="show_tests"),
    # path('user/setup/<int:user_id>', user_setup, name='user_setup'),
]

