# Generated by Django 4.1.3 on 2022-12-23 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0002_room_remove_chatuser_rooms_remove_chatuser_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="users",
            field=models.ManyToManyField(
                related_name="rooms", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("handle", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.room"
                    ),
                ),
            ],
        ),
    ]
