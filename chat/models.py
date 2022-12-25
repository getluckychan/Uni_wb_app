from django.db import models

# Create your models here.
from vnz.models import *


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    users = models.ManyToManyField(MyUser, related_name="rooms")


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    handle = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    def last_10_messages(room):
        return Message.objects.order_by('-timestamp').filter(room=room)[:10]

    def __str__(self):
        return self.handle

