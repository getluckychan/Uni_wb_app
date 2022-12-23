from django.urls import re_path, path

from . import consumers
# from .views import RoomListView, UserSearchForChatView

websocket_urlpatterns = [
    re_path(r"ws/chat/entered/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

