import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async # Implement later


from vnz.models import MyUser


@database_sync_to_async
def get_user(user_id):
    try:
        return MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        return AnonymousUser()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        self.user = await get_user(self.scope["user"].id)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "user": user}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user": user}))


