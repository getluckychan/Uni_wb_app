# Generated by Django 4.1.3 on 2022-12-23 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vnz", "0012_myuser_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="educator",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="student",
            name="photo",
        ),
    ]
