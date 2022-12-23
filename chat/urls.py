from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path("", index, name="chat_main"),
    path("entered/<str:room_name>/", room, name="room"),
    path("wtf/", RoomListView.as_view(), name="room_list"),
    # path("search/", UserSearchForChatView.as_view(), name="user_search"),
]